import datetime
from decimal import Decimal
from typing import Optional
from model_utils import Choices
from django_extensions.db.fields import AutoSlugField

from django.db import models
from django.db.models import Case, When, F, ExpressionWrapper, Value, Q
from django.db.models.functions import ExtractYear, Concat, Cast
from django.core.validators import ValidationError
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.urls import reverse

from backend.users.models import User
from backend.groups.models import JANUNGroup
from backend.utils import slugify_german

from .states import STATES_CONFIRMED, STATES_REJECTED, STATES


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
            self.annotate(year=ExtractYear("start_date"))
            .annotate(
                planned_attendence_days=F("planned_attendees_max")
                * F("planned_training_days"),
                deadline=Case(
                    When(
                        start_date__quarter=1,
                        then=Concat(Cast("year", models.TextField()), Value("-04-15")),
                    ),
                    When(
                        start_date__quarter=2,
                        then=Concat(Cast("year", models.TextField()), Value("-07-15")),
                    ),
                    When(
                        start_date__quarter=3,
                        then=Concat(Cast("year", models.TextField()), Value("-10-15")),
                    ),
                    When(
                        start_date__quarter=4,
                        then=Concat(
                            Cast("year", models.TextField()) + 1, Value("-01-15")
                        ),
                    ),
                    output_field=models.DateField(),
                ),
            )
            .annotate(
                deadline_applicable=Case(
                    When(
                        status__in=("angemeldet", "zugesagt", "stattgefunden"),
                        then=True,
                    ),
                    default=False,
                    output_field=models.BooleanField(),
                ),
                funding=Case(
                    When(actual_funding__isnull=True, then="requested_funding"),
                    default="actual_funding",
                ),
                tnt=Case(
                    When(
                        actual_attendence_days_total__isnull=True,
                        then="planned_attendence_days",
                    ),
                    default="actual_attendence_days_total",
                ),
                tnt_cost=ExpressionWrapper(
                    F("funding") / F("tnt"), output_field=models.DecimalField()
                ),
                attendees=Case(
                    When(
                        actual_attendees_total__isnull=True,
                        then="planned_attendees_max",
                    ),
                    default="actual_attendees_total",
                ),
                training_days=Case(
                    When(
                        actual_training_days__isnull=True, then="planned_training_days"
                    ),
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
                deadline_status=Case(
                    When(
                        Q(deadline_applicable=True) & Q(deadline__lte=timezone.now()),
                        then=Value("expired"),
                    ),
                    When(
                        Q(deadline_applicable=True)
                        & Q(deadline__lte=timezone.now() - datetime.timedelta(days=14)),
                        then=Value("soon"),
                    ),
                    When(
                        Q(deadline_applicable=True)
                        & Q(deadline__gt=timezone.now() - datetime.timedelta(days=14)),
                        then=Value("not_soon"),
                    ),
                    When(deadline_applicable=False, then=Value("not_applicable")),
                    default=Value("unknown"),
                    output_field=models.CharField(),
                ),
                expense_minus_income=Coalesce("expense_total", 0)
                - Coalesce("income_total", 0),
            )
        )

    def is_confirmed(self):
        return self.filter(status__in=(STATES_CONFIRMED))

    def is_rejected(self):
        return self.filter(status__in=(STATES_REJECTED))
    
    def is_not_rejected(self):
        return self.exclude(status__in=(STATES_REJECTED))

    def last_year(self):
        return self.filter(start_date__year=timezone.now().year - 1)

    def this_year(self):
        return self.filter(start_date__year=timezone.now().year)

    def next_year(self):
        return self.filter(start_date__year=timezone.now().year + 1)


class SeminarManager(models.Manager.from_queryset(SeminarQuerySet)):
    def get_queryset(self):
        return super().get_queryset().add_annotations()


class Seminar(models.Model):
    STATE_CHOICES = Choices(*STATES)

    title = models.CharField("Titel", max_length=255)
    slug = AutoSlugField(
        "URL-Titel",
        populate_from="title",
        max_length=100,
        unique=True,
        null=True,
        editable=False,
        slugify_function=slugify_german,
    )
    status = models.CharField(
        "Status",
        max_length=255,
        choices=STATE_CHOICES,
        default=STATE_CHOICES.angemeldet,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
    location = models.CharField(
        "Ort",
        max_length=255,
        blank=True,
        help_text="Stadt, in der das Seminar stattfindet",
    )
    planned_training_days = models.PositiveSmallIntegerField(
        "geplante Bildungstage", null=True, blank=True
    )
    planned_attendees_min = models.PositiveSmallIntegerField(
        "geplante Teilnehmende min.", null=True, blank=True
    )
    planned_attendees_max = models.PositiveSmallIntegerField(
        "geplante Teilnehmende max.", null=True, blank=True
    )
    requested_funding = models.DecimalField(
        "gewünschte Förderung", max_digits=10, decimal_places=2, null=True, blank=True
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
    transferred_at = models.DateField("überwiesen am", blank=True, null=True)
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

    objects = SeminarManager()

    def __str__(self) -> str:
        return "{0} am {1}".format(self.title, self.start_date.strftime("%d.%m.%Y"))

    def get_absolute_url(self):
        return reverse(
            "seminar_detail", kwargs={"slug": self.slug, "year": self.start_date.year}
        )

    def get_admin_change_url(self):
        return reverse("admin:seminars_seminar_change", args=(self.pk,))

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "End-Datum muss nach Start-Datum liegen."}
            )
        if (
            self.planned_attendees_max
            and self.planned_attendees_min
            and self.planned_attendees_max < self.planned_attendees_min
        ):
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

    @property
    def was_edited(self):
        return self.updated_at - self.created_at > datetime.timedelta(seconds=1)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"

    def __str__(self) -> str:
        return self.text
