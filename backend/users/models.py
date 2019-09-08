from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from model_utils import Choices

from backend.groups.models import JANUNGroup


class CaseInsensitiveUserManager(UserManager):
    "User Manager that when getting users by their username ignores case"

    def get_by_natural_key(self, username):
        case_insensitive_username_field = "{}__iexact".format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    ROLES = Choices("Teamer_in", "Prüfer_in", "Verwalter_in")
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    name = models.CharField(max_length=255)
    address = models.TextField("Post-Adresse", blank=True)
    telephone = models.CharField("Telefon-Nummer", max_length=100, blank=True)
    role = models.CharField(
        "Rolle", max_length=255, choices=ROLES, default=ROLES["Teamer_in"]
    )
    is_reviewed = models.BooleanField("überprüft?", default=False)
    janun_groups = models.ManyToManyField(
        JANUNGroup, related_name="members", blank=True, verbose_name="JANUN-Gruppen"
    )
    group_hats = models.ManyToManyField(
        JANUNGroup, related_name="group_hats", blank=True, verbose_name="Gruppenhüte"
    )
    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Geändert am", auto_now=True)

    objects = CaseInsensitiveUserManager()
    EMAIL_FIELD = "email"

    class Meta:
        ordering = ("name",)
        verbose_name = "Konto"
        verbose_name_plural = "Konten"

    def __str__(self) -> str:
        return self.username

    @property
    def has_staff_role(self) -> bool:
        return self.role in ("Prüfer_in", "Verwalter_in")

    @property
    def has_verwalter_role(self) -> bool:
        return self.role == "Verwalter_in"
