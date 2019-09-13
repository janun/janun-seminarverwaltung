import datetime
from decimal import Decimal
from typing import Optional
from model_utils import Choices

from django.db import models
from django.db.models import Case, When, F, ExpressionWrapper
from django.core.validators import ValidationError
from django.db.models.functions import Coalesce

from backend.users.models import User
from backend.groups.models import JANUNGroup


def get_quarter(date: datetime.date) -> int:
    return (date.month - 1) // 3


def add_none(*p) -> Optional[Decimal]:
    """treat None values as 0, return None if all args are None"""
    if all(v is None for v in p):
        return None
    return sum(filter(None, p))


class SeminarQuerySet(models.QuerySet):
    def add_annotations(self):
        return (
            self.annotate(
                planned_attendence_days=F("planned_attendees_max")
                * F("planned_training_days")
            )
            .annotate(
                funding=Case(
                    When(actual_funding=None, then="requested_funding"),
                    default="actual_funding",
                ),
                tnt=Case(
                    When(
                        actual_attendence_days_total=None,
                        then="planned_attendence_days",
                    ),
                    default="actual_attendence_days_total",
                ),
                tnt_cost=ExpressionWrapper(
                    F("funding") / F("tnt"), output_field=models.DecimalField()
                ),
                attendees=Case(
                    When(actual_attendees_total=None, then="planned_attendees_max"),
                    default="actual_attendees_total",
                ),
                training_days=Case(
                    When(actual_training_days=None, then="planned_training_days"),
                    default="actual_training_days",
                ),
                income_total=Coalesce("income_fees", 0)
                + Coalesce("income_public", 0)
                + Coalesce("income_other", 0),
                expense_total=Coalesce("expense_accomodation", 0)
                + Coalesce("expense_catering", 0)
                + Coalesce("expense_other", 0)
                + Coalesce("expense_referent", 0)
                + Coalesce("expense_travel", 0),
            )
            .annotate(
                expense_minus_income=Coalesce("expense_total", 0)
                - Coalesce("income_total", 0)
            )
        )


class SeminarManager(models.Manager.from_queryset(SeminarQuerySet)):
    def get_queryset(self):
        return super().get_queryset().add_annotations()


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

    deadline = models.DateField(
        "Abrechnungsdeadline", help_text="Aus End-Datum errechnet"
    )

    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Geändert am", auto_now=True)

    class Meta:
        ordering = ("-start_date",)
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"

    objects = SeminarManager()

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
        if (
            self.actual_attendees_jfg
            and self.actual_attendees_total
            and self.actual_attendees_jfg > self.actual_attendees_total
        ):
            raise ValidationError(
                {"actual_attendees_jfg": "Muss kleiner/gleich sein als der Gesamt-Wert"}
            )
        if (
            self.actual_attendence_days_jfg
            and self.actual_attendence_days_total
            and self.actual_attendence_days_jfg > self.actual_attendence_days_total
        ):
            raise ValidationError(
                {"actual_attendees_jfg": "Muss kleiner/gleich sein als der Gesamt-Wert"}
            )

    def save(self, *args, **kwargs):
        self.deadline = self.calc_deadline()
        super().save(*args, **kwargs)

    def calc_deadline(self) -> datetime.date:
        quarter = get_quarter(self.end_date)
        year = self.end_date.year
        deadlines = [
            datetime.date(year, 4, 15),
            datetime.date(year, 7, 15),
            datetime.date(year, 10, 15),
            datetime.date(year + 1, 1, 15),
        ]
        return deadlines[quarter]

    # def get_income_total(self) -> Optional[Decimal]:
    #     return add_none(self.income_fees, self.income_public, self.income_other)

    # get_income_total.short_description = "Gesamt-Einnahmen"
    # income_total = property(get_income_total)

    # def get_expense_total(self) -> Optional[Decimal]:
    #     return add_none(
    #         self.expense_accomodation,
    #         self.expense_catering,
    #         self.expense_other,
    #         self.expense_referent,
    #         self.expense_travel,
    #     )

    # get_expense_total.short_description = "Gesamt-Ausgaben"
    # expense_total = property(get_expense_total)

    # def get_expense_minus_income(self) -> Optional[Decimal]:
    #     if not self.expense_total and not self.income_total:
    #         return None
    #     if not self.income_total:
    #         return self.expense_total
    #     if not self.expense_total:
    #         return -self.income_total
    #     return self.expense_total - self.income_total

    # get_expense_minus_income.short_description = "Ausgaben minus Einnahmen"
    # expense_minus_income = property(get_expense_minus_income)


class SeminarComment(models.Model):
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
    is_internal = models.BooleanField("intern?", default=False)

    created_at = models.DateTimeField("Erstellt am", auto_now_add=True)
    updated_at = models.DateTimeField("Geändert am", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"

    def __str__(self) -> str:
        return self.text
