from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.apps import apps
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

import rules

from phonenumber_field.modelfields import PhoneNumberField

from model_utils import Choices


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username="", email="", password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.update({'username': username})
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


def avatar_filename(instance, filename):
    return "avatars/{0}/{1}".format(instance.name, filename)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        "Voller Name", max_length=255
    )
    email = models.EmailField(
        "E-Mail-Adresse", unique=True,
        help_text="Wichtig für Kontakt. Kann auch zum Anmelden verwendet werden"
    )
    username = models.CharField(
        "Benutzername", max_length=40, blank=True, null="True",
        help_text=""
    )
    avatar = models.ImageField(
        verbose_name="Profilbild", blank=True, null=True,
        upload_to=avatar_filename
    )
    phone_number = PhoneNumberField("Telefonnummer", blank=True)
    address = models.TextField("Postadresse", blank=True, null=True)
    is_staff = models.BooleanField("Admin-Zugang", default=False)
    is_active = models.BooleanField("aktiv", default=True)
    date_joined = models.DateTimeField("beigetreten", default=timezone.now)
    is_reviewed = models.BooleanField(
        "überprüft", default=False,
        help_text="Darf erst auf Gruppendaten zugreifen, wenn überprüft."
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    ROLES = Choices(
        ('TEAMER', 'Teamer_in'),
        ('PRUEFER', 'Prüfer_in'),
        ('VERWALTER', 'Verwalter_in'),
    )

    role = models.CharField(
        verbose_name="Rolle",
        max_length=100,
        choices=ROLES,
        default='TEAMER',
    )

    janun_groups = models.ManyToManyField(
        'groups.JANUNGroup',
        blank=True,
        related_name="members",
        verbose_name="Gruppen-Mitgliedschaften",
    )

    group_hats = models.ManyToManyField(
        'groups.JANUNGroup',
        blank=True,
        related_name="group_hats",
        verbose_name="Gruppenhüte",
    )

    objects = UserManager()

    @property
    def is_teamer(self):
        return self.role == 'TEAMER'

    @property
    def is_verwalter(self):
        return self.role == 'VERWALTER'

    @property
    def is_pruefer(self):
        return self.role == 'PRUEFER'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        if self.username:
            qs = User.objects.filter(username=self.username)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({
                    'username': "Es existiert schon ein Benutzer mit diesem Benutzernamen",
                })

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username or self.name.partition(' ')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.name or self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"pk": self.pk})

    def get_groups(self):
        # TODO: union of janun_groups and group_hats?
        if self.role == "TEAMER":
            return self.janun_groups.all()
        if self.role in ("PRUEFER", "VERWALTER"):
            return self.group_hats.all()
        return []

    def get_seminars(self):
        Seminar = apps.get_model('seminars', 'Seminar')
        if self.role == 'VERWALTER':
            return Seminar.objects.all()
        return Seminar.objects.filter(
            Q(author=self)
            | Q(group__in=self.group_hats.all())
            | Q(group__in=self.janun_groups.all())
        )


    class Meta:
        verbose_name = "Benutzer_in"
        verbose_name_plural = "Benutzer_innen"
        permissions = (
            ('detail_user', "Kann Benutzerdaten sehen"),
            ('see_all_users', "Kann alle Benutzer sehen")
        )


def get_verwalter_mails():
    qs = User.objects.filter(role='VERWALTER')
    return list(qs.values_list('email', flat=True))


def get_group_hat_mails(group):
    qs = User.objects.filter(group_hats=group)
    return list(qs.values_list('email', flat=True))


@rules.predicate
def is_teamer(user):
    return user.role == "TEAMER"

@rules.predicate
def is_pruefer(user):
    return user.role == "PRUEFER"

@rules.predicate
def is_verwalter(user):
    return user.role == "VERWALTER"

@rules.predicate
def is_own_user(user, obj):
    return user == obj

@rules.predicate
def is_in_same_group(user, obj):
    return any(group in obj.get_groups() for group in user.get_groups())

@rules.predicate
def is_reviewed(user):
    return user.is_reviewed

rules.add_perm('users.see_all_users', is_verwalter | is_pruefer)
rules.add_perm('users.detail_user', is_verwalter | is_own_user | is_pruefer | is_in_same_group & is_reviewed)
rules.add_perm('users.add_user', is_verwalter | is_pruefer)
rules.add_perm('users.change_user', is_verwalter | is_pruefer | is_own_user)
rules.add_perm('users.change_permissions', is_verwalter | is_pruefer)
rules.add_perm('users.delete_user', is_verwalter)
rules.add_perm('users.deactivate_user', is_verwalter | is_pruefer)
rules.add_perm('users.review', is_verwalter | is_pruefer)
