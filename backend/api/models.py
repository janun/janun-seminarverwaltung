import datetime
from decimal import Decimal
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.text import slugify

from model_utils import Choices

from .utils import get_quarter


def change_api_updated_at(*args, **kwargs) -> None:
    cache.set("api_updated_at_timestamp", datetime.datetime.utcnow())


class JANUNGroup(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)


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
    address = models.TextField(blank=True)
    role = models.CharField(max_length=255, choices=ROLES, default=ROLES["Teamer_in"])
    telephone = models.CharField(max_length=100, blank=True)
    is_reviewed = models.BooleanField(default=False)
    janun_groups = models.ManyToManyField(
        JANUNGroup, related_name="members", blank=True
    )
    group_hats = models.ManyToManyField(
        JANUNGroup, related_name="group_hats", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_visit = models.DateTimeField(null=True)

    objects = CaseInsensitiveUserManager()
    EMAIL_FIELD = "email"

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.username

    @property
    def has_staff_role(self) -> bool:
        return self.role in ("Prüfer_in", "Verwalter_in")

    @property
    def has_verwalter_role(self) -> bool:
        return self.role == "Verwalter_in"


class Seminar(models.Model):
    # manual data migrations needed if STATES changed
    STATES = Choices(
        "angemeldet",
        "zurückgezogen",
        "zugesagt",
        "abgelehnt",
        "abgesagt",
        "stattgefunden",
        "ohne Abrechnung",
        "Abrechnung abgeschickt",
        "Abrechnung angekommen",
        "Abrechnung unmöglich",
        "rechnerische Prüfung",
        "inhaltliche Prüfung",
        "Zweitprüfung",
        "fertig geprüft",
        "überwiesen",
    )

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATES, default=STATES.angemeldet)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="seminars"
    )
    group = models.ForeignKey(
        JANUNGroup, on_delete=models.SET_NULL, null=True, related_name="seminars"
    )

    description = models.TextField(blank=True)

    start_date = models.DateField(db_index=True)
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField()
    end_time = models.TimeField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True)

    planned_training_days = models.PositiveSmallIntegerField()
    planned_attendees_min = models.PositiveSmallIntegerField()
    planned_attendees_max = models.PositiveSmallIntegerField()
    requested_funding = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-start_date",)

    def __str__(self) -> str:
        return self.title

    @property
    def tnt(self) -> int:
        return self.planned_attendees_max * self.planned_training_days

    @property
    def tnt_cost(self) -> Decimal:
        if self.tnt == 0:
            return Decimal("0")
        return (self.requested_funding / self.tnt).quantize(Decimal("1.00"))

    @property
    def deadline(self) -> datetime.date:
        quarter = get_quarter(self.end_date)
        year = self.end_date.year
        deadlines = [
            datetime.date(year, 4, 15),
            datetime.date(year, 7, 15),
            datetime.date(year, 10, 15),
            datetime.date(year + 1, 1, 15),
        ]
        return deadlines[quarter]

    @property
    def deadline_expired(self) -> bool:
        not_sent = self.status in ("angemeldet", "zugesagt", "stattgefunden")
        expired = self.deadline < datetime.date.today()
        return expired and not_sent

    @property
    def deadline_in_two_weeks(self) -> bool:
        not_sent = self.status in ("angemeldet", "zugesagt", "stattgefunden")
        in_two_weeks: bool = self.deadline < datetime.date.today() + datetime.timedelta(
            days=14
        )
        return in_two_weeks and not_sent and not self.deadline_expired


for model in [Seminar]:
    post_save.connect(receiver=change_api_updated_at, sender=model)
    post_delete.connect(receiver=change_api_updated_at, sender=model)


class SeminarComment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    seminar = models.ForeignKey(
        Seminar, on_delete=models.CASCADE, related_name="comments"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.text
