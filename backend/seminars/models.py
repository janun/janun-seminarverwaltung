import uuid
import datetime
from decimal import Decimal

from django.db import models
from model_utils import Choices
from django.core.validators import MinValueValidator

from backend.users.models import User
from backend.groups.models import JANUNGroup


def get_quarter(date: datetime.date) -> int:
    return (date.month - 1) // 3


class SeminarIncomeRecord(models.Model):
    seminar = models.ForeignKey(
        "seminars.Seminar", on_delete=models.SET_NULL, null=True, related_name="incomes"
    )
    amount = models.DecimalField(
        "Betrag",
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    name = models.CharField("Bezeichnung", max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name = "Einnahme"
        verbose_name_plural = "Einnahmen"

    def __str__(self) -> str:
        return f"{self.name} ({self.amount})"


class SeminarExpenseRecord(models.Model):
    seminar = models.ForeignKey(
        "seminars.Seminar",
        on_delete=models.SET_NULL,
        null=True,
        related_name="expenses",
    )
    amount = models.DecimalField(
        "Betrag",
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    name = models.CharField("Bezeichnung", max_length=255)

    class Meta:
        ordering = ("name",)
        verbose_name = "Ausgabe"
        verbose_name_plural = "Ausgaben"

    def __str__(self) -> str:
        return f"{self.name} ({self.amount})"


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
    title = models.CharField("Titel", max_length=255)
    status = models.CharField(
        "Status", max_length=255, choices=STATES, default=STATES.angemeldet
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="seminars",
        verbose_name="Eigentümer",
    )
    group = models.ForeignKey(
        JANUNGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seminars",
        verbose_name="JANUN-Gruppe",
    )
    description = models.TextField("Beschreibung", blank=True)
    start_date = models.DateField("Start-Datum", db_index=True)
    start_time = models.TimeField("Start-Zeit", blank=True, null=True)
    end_date = models.DateField("End-Datum")
    end_time = models.TimeField("End-Zeit", blank=True, null=True)
    location = models.CharField("Ort", max_length=255, blank=True)
    planned_training_days = models.PositiveSmallIntegerField("geplante Bildungstage")
    planned_attendees_min = models.PositiveSmallIntegerField("geplante TN min.")
    planned_attendees_max = models.PositiveSmallIntegerField("geplante TN max.")
    requested_funding = models.DecimalField(
        "angeforderte Förderung", max_digits=10, decimal_places=2
    )

    # Abrechnungsfelder:
    attendees_total = models.PositiveSmallIntegerField(
        "TN insgesamt", blank=True, null=True
    )
    attendees_jfg = models.PositiveSmallIntegerField(
        "TN nach JFG", blank=True, null=True
    )
    attendence_days_total = models.PositiveSmallIntegerField(
        "TNT insgesamt", blank=True, null=True
    )
    attendence_days_jfg = models.PositiveSmallIntegerField(
        "TNT nach JFG", blank=True, null=True
    )
    advance = models.DecimalField(
        "Vorschuss", max_digits=10, decimal_places=2, default=0
    )
    training_days = models.PositiveSmallIntegerField(
        "Bildungstage", blank=True, null=True
    )
    funding = models.DecimalField(
        "Förderbedarf", max_digits=10, decimal_places=2, blank=True, null=True
    )

    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Geändert am", auto_now=True)

    class Meta:
        ordering = ("-start_date",)
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"

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

    @property
    def incomes_total(self) -> Decimal:
        return sum(income.amount for income in self.incomes)

    @property
    def expenses_total(self) -> Decimal:
        return sum(expense.amount for expense in self.expenses)

    @property
    def balance(self) -> Decimal:
        return self.incomes_total - self.expenses_total


class SeminarComment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
        verbose_name="Autor",
    )
    seminar = models.ForeignKey(
        Seminar, on_delete=models.CASCADE, related_name="comments"
    )

    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Geändert am", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"

    def __str__(self) -> str:
        return self.text
