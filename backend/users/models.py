from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from allauth_2fa.utils import user_has_valid_totp_device
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField
from preferences.models import Preferences
from simple_history.models import HistoricalRecords

from backend.groups.models import JANUNGroup


class JANUNSeminarPreferences(Preferences):
    help_phone = PhoneNumberField("Hilfe-Telefon", blank=True)
    help_email = models.EmailField("Hilfe-E-Mail", blank=True)
    seminar_policy_url = models.URLField("Link Seminarrichtlinie", blank=True)
    data_protection_policy_url = models.URLField(
        "Link Datenschutzrichtlinie", blank=True
    )
    legal_url = models.URLField(
        "Link zum Impressum", default="https://www.janun.de/impressum"
    )
    history = HistoricalRecords()

    def __str__(self) -> str:
        return "Einstellungen"

    def get_absolute_url(self) -> str:
        return ""

    class Meta:
        verbose_name = "Einstellung"
        verbose_name_plural = "Einstellungen"


class CaseInsensitiveUserManager(UserManager):
    "User Manager that when getting users by their username ignores case"

    def get_by_natural_key(self, username):
        case_insensitive_username_field = "{}__iexact".format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    ROLES = Choices("Teamer_in", "Prüfer_in", "Verwalter_in")
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    name = models.CharField("Voller Name", max_length=255)
    telephone = PhoneNumberField(
        "Telefonnummer",
        error_messages={
            "invalid": "Bitte gültige Telefonnummer eingeben, z.B. 0511 1241512"
        },
        blank=True,
    )
    role = models.CharField(
        "Rolle", max_length=255, choices=ROLES, default=ROLES.Teamer_in
    )
    is_reviewed = models.BooleanField("überprüft", default=False)
    janun_groups = models.ManyToManyField(
        JANUNGroup, related_name="members", blank=True, verbose_name="JANUN-Gruppen"
    )
    group_hats = models.ManyToManyField(
        JANUNGroup, related_name="group_hats", blank=True, verbose_name="Gruppenhüte"
    )
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Geändert am", auto_now=True)
    last_visit = models.DateTimeField("Letzter Besuch", null=True)

    objects = CaseInsensitiveUserManager()
    history = HistoricalRecords(
        excluded_fields=["last_visit", "last_login", "updated_at"]
    )
    EMAIL_FIELD = "email"

    class Meta:
        ordering = ("name",)
        verbose_name = "Konto"
        verbose_name_plural = "Konten"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        # auto set is_staff and is_superuser
        if self.is_reviewed:
            self.is_staff = self.role in (self.ROLES.Verwalter_in, self.ROLES.Prüfer_in)
            self.is_superuser = self.role == self.ROLES.Verwalter_in
        super().save(*args, **kwargs)

    def get_full_name(self) -> str:
        return self.name

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )

    @property
    def has_totp(self):
        return user_has_valid_totp_device(self)
