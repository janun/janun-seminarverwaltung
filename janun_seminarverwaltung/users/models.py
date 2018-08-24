from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.apps import apps

import rules

from model_utils import Choices

# from seminars.models import Seminar


def avatar_filename(instance, filename):
    return "avatars/{0}/{1}".format(instance.name, filename)


class User(AbstractUser):
    name = models.CharField("Voller Name", blank=True, max_length=255)
    avatar = models.ImageField(
        verbose_name="Profilbild", blank=True, null=True,
        upload_to=avatar_filename
    )

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

    # for TEAMER
    janun_groups = models.ManyToManyField(
        'groups.JANUNGroup',
        blank=True,
        related_name="members",
        verbose_name="Gruppe(n)",
        help_text="JANUN-Gruppe(n), in denen der_die Teamer_in Mitglied ist",
    )

    # for PRUEFER
    group_hats = models.ManyToManyField(
        'groups.JANUNGroup',
        blank=True,
        related_name="group_hats",
        verbose_name="Gruppenhüte",
        help_text="JANUN-Gruppe(n), für die der_die Prüfer_in einen Gruppenhut hat",
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_groups(self):
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
        permissions = (
            ('detail_user', "Kann Benutzerdaten sehen"),
            ('can_see_all_users', "Kann alle Benutzer sehen")
        )


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


rules.add_perm('users.can_see_all_users', is_verwalter)
rules.add_perm('users.detail_user', is_verwalter | is_own_user | is_in_same_group)
rules.add_perm('users.add_user', is_verwalter)
rules.add_perm('users.change_user', is_verwalter | is_own_user)
rules.add_perm('users.delete_user', is_verwalter)
