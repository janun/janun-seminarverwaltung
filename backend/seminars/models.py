import uuid
import datetime
from decimal import Decimal
from typing import Optional

from django.db import models
from django.core.validators import ValidationError
from model_utils import Choices

from backend.users.models import User
from backend.groups.models import JANUNGroup


def get_quarter(date: datetime.date) -> int:
    return (date.month - 1) // 3


def add_none(*p) -> Optional[Decimal]:
    """treat None values as 0, return None if all args are None"""
    if all(v is None for v in p):
        return None
    return sum(filter(None, p))


class Seminar(models.Model):
    STATES = Choices(
        "angemeldet",
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
        verbose_name="Eigentümer_in",
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
    actual_attendees_total = models.PositiveSmallIntegerField(
        "TN insgesamt", blank=True, null=True
    )
    actual_attendees_jfg = models.PositiveSmallIntegerField(
        "TN nach JFG", blank=True, null=True
    )
    actual_attendence_days_total = models.PositiveSmallIntegerField(
        "TNT insgesamt", blank=True, null=True
    )
    actual_attendence_days_jfg = models.PositiveSmallIntegerField(
        "TNT nach JFG", blank=True, null=True
    )
    advance = models.DecimalField(
        "Vorschuss", max_digits=10, decimal_places=2, blank=True, null=True
    )
    actual_training_days = models.PositiveSmallIntegerField(
        "Bildungstage", blank=True, null=True
    )
    actual_funding = models.DecimalField(
        "Förderbedarf", max_digits=10, decimal_places=2, blank=True, null=True
    )
    expense_catering = models.DecimalField(
        "Ausgaben für Verpflegung",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    expense_accomodation = models.DecimalField(
        "Ausgaben für Unterkunft",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    def get_expense_accomodation_and_catering(self) -> Optional[Decimal]:
        return add_none(self.expense_catering, self.expense_accomodation)

    get_expense_accomodation_and_catering.short_description = (
        "Ausgaben für Unterkunft und Verpflegung"
    )
    expense_accomodation_and_catering = property(get_expense_accomodation_and_catering)

    expense_referent = models.DecimalField(
        "Ausgaben für Referent_innen",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    expense_travel = models.DecimalField(
        "Fahrtkosten", max_digits=10, decimal_places=2, blank=True, null=True
    )
    expense_other = models.DecimalField(
        "Sonstige Ausgaben", max_digits=10, decimal_places=2, blank=True, null=True
    )
    income_fees = models.DecimalField(
        "Teilnahmebeiträge", max_digits=10, decimal_places=2, blank=True, null=True
    )
    income_public = models.DecimalField(
        "Öffentliche Zuwendungen",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    income_other = models.DecimalField(
        "Sonstige Einnahmen", max_digits=10, decimal_places=2, blank=True, null=True
    )

    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Geändert am", auto_now=True)

    class Meta:
        ordering = ("-start_date",)
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "End-Datum muss nach Start-Datum liegen."}
            )
        if self.planned_attendees_max < self.planned_attendees_min:
            raise ValidationError(
                {
                    "planned_attendees_max": "Muss größer/gleich "
                    "sein als der Minimal-Wert"
                }
            )
        if self.actual_attendees_jfg > self.actual_attendees_total:
            raise ValidationError(
                {"actual_attendees_jfg": "Muss kleiner/gleich sein als der Gesamt-Wert"}
            )
        if self.actual_attendence_days_jfg > self.actual_attendence_days_total:
            raise ValidationError(
                {"actual_attendees_jfg": "Muss kleiner/gleich sein als der Gesamt-Wert"}
            )

    @property
    def planned_tnt(self) -> int:
        return self.planned_attendees_max * self.planned_training_days

    def get_tnt(self) -> int:
        return self.actual_attendence_days_total or self.planned_tnt

    get_tnt.short_description = "TNT"
    tnt = property(get_tnt)

    def get_attendees(self) -> int:
        return self.actual_attendees_total or self.planned_attendees_max

    get_attendees.short_description = "TN"
    attendees = property(get_attendees)

    def get_funding(self) -> Decimal:
        return self.actual_funding or self.requested_funding

    get_funding.short_description = "Förderung"
    funding = property(get_funding)

    def get_training_days(self) -> int:
        return self.actual_training_days or self.planned_training_days

    get_training_days.short_description = "Bildungstage"
    training_days = property(get_training_days)

    @property
    def tnt_cost(self) -> Optional[Decimal]:
        if self.tnt == 0:
            return None
        return (self.funding / self.tnt).quantize(Decimal("1.00"))

    def get_deadline(self) -> datetime.date:
        quarter = get_quarter(self.end_date)
        year = self.end_date.year
        deadlines = [
            datetime.date(year, 4, 15),
            datetime.date(year, 7, 15),
            datetime.date(year, 10, 15),
            datetime.date(year + 1, 1, 15),
        ]
        return deadlines[quarter]

    get_deadline.short_description = "Abrechnungsdeadline"
    deadline = property(get_deadline)

    def get_deadline_expired(self) -> bool:
        not_sent = self.status in ("angemeldet", "zugesagt", "stattgefunden")
        expired = self.deadline < datetime.date.today()
        return expired and not_sent

    get_deadline_expired.short_description = "Deadline abgelaufen"
    deadline_expired = property(get_deadline_expired)

    def get_deadline_in_two_weeks(self) -> bool:
        not_sent = self.status in ("angemeldet", "zugesagt", "stattgefunden")
        in_two_weeks: bool = self.deadline < datetime.date.today() + datetime.timedelta(
            days=14
        )
        return in_two_weeks and not_sent and not self.deadline_expired

    get_deadline_in_two_weeks.short_description = "Deadline in den nächsten 2 Wochen"
    deadline_in_two_weeks = property(get_deadline_in_two_weeks)

    def get_income_total(self) -> Optional[Decimal]:
        return add_none(self.income_fees, self.income_public, self.income_other)

    get_income_total.short_description = "Gesamt-Einnahmen"
    income_total = property(get_income_total)

    def get_expense_total(self) -> Optional[Decimal]:
        return add_none(
            self.expense_accomodation,
            self.expense_catering,
            self.expense_other,
            self.expense_referent,
            self.expense_travel,
        )

    get_expense_total.short_description = "Gesamt-Ausgaben"
    expense_total = property(get_expense_total)


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
