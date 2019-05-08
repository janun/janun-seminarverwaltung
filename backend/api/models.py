import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from model_utils import Choices

from .utils import get_quarter


def change_api_updated_at(*args, **kwargs) -> None:
    cache.set("api_updated_at_timestamp", datetime.datetime.utcnow())


class JANUNGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)


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

    is_reviewed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    EMAIL_FIELD = "email"

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.username


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


for model in [Seminar]:
    post_save.connect(receiver=change_api_updated_at, sender=model)
    post_delete.connect(receiver=change_api_updated_at, sender=model)


class SeminarComment(models.Model):
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
