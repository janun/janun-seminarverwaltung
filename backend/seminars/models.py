import datetime
from decimal import Decimal
from typing import Optional
from model_utils import Choices
from django_extensions.db.fields import AutoSlugField
import formulas
from formulas.errors import FormulaError

from django.db import models
from django.db.models import Case, When, F, ExpressionWrapper, Value, Q
from django.db.models.functions import ExtractYear, Concat, Cast
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist

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


class FundingRate(models.Model):
    year = models.IntegerField("Jahr")

    group_rate = models.DecimalField(
        "Satz für Gruppen", max_digits=10, decimal_places=2
    )
    group_rate_one_day = models.DecimalField(
        "Satz für Gruppen für Eintagesseminare",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    group_limit_formula = models.CharField(
        "Formel für Gruppen-Limit",
        max_length=255,
        help_text="engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450)",
        blank=True,
    )
    group_limit = models.DecimalField(
        "Gruppen-Limit",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        help_text="Hat Vorrang vor der Formel",
    )

    single_rate = models.DecimalField(
        "Satz für Einzelpersonen", max_digits=10, decimal_places=2
    )
    single_rate_one_day = models.DecimalField(
        "Satz für Einzelpersonen für Eintagesseminare",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    single_limit_formula = models.CharField(
        "Formel für Einzelpersonen-Limit",
        max_length=255,
        help_text="engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450)",
        blank=True,
    )
    single_limit = models.DecimalField(
        "Einzelpersonen-Limit",
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=2,
        help_text="Hat Vorrang vor der Formel",
    )

    def test_formula(self, formula):
        formulas.Parser().ast(formula)[1].compile()

    def clean(self):
        if self.single_limit_formula:
            try:
                self.test_formula(self.single_limit_formula)
            except FormulaError as error:
                raise ValidationError({"single_limit_formula": error})

        if self.group_limit_formula:
            try:
                self.test_formula(self.group_limit_formula)
            except FormulaError as error:
                raise ValidationError({"group_limit_formula": error})

    def get_rate(self, has_group: bool, days: int) -> Decimal:
        if has_group:
            if days == 1:
                return self.group_rate_one_day
            return self.group_rate
        if days == 1:
            return self.single_rate_one_day
        return self.single_rate

    def limit(self, seminar, funding: Decimal) -> Decimal:
        upper_limit = self.group_limit if seminar.group else self.single_limit
        if upper_limit and funding > upper_limit:
            return upper_limit

        formula = (
            self.group_limit_formula if seminar.group else self.single_limit_formula
        )
        if formula:
            lower_limit = (
                formulas.Parser()
                .ast(formula)[1]
                .compile()(B=seminar.planned_training_days)
            )
            if lower_limit and funding > lower_limit:
                return lower_limit

        return funding

    def get_max_funding(self, seminar) -> Decimal:
        if seminar.planned_training_days and seminar.planned_attendees_max:
            rate = self.get_rate(seminar.group, seminar.planned_training_days)
            tnt = seminar.planned_training_days * seminar.planned_attendees_max
            funding = rate * tnt
            return self.limit(seminar, funding)

    def __str__(self):
        return "%s" % self.year

    class Meta:
        verbose_name = "Förderungssatz"
        verbose_name_plural = "Förderungssätze"


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
                            Cast(F("year") + 1, models.TextField()), Value("-01-15")
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

    def clean(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError(
                    {"end_date": "Muss größer/gleich Start-Datum sein"}
                )
            if self.end_date == self.start_date and self.start_time and self.end_time:
                if self.end_time < self.start_time:
                    raise ValidationError(
                        {"end_time": "Muss größer/gleich Start-Zeit sein"}
                    )
            if self.planned_training_days:
                days = (self.end_date - self.start_date).days + 1
                if self.planned_training_days > days:
                    raise ValidationError(
                        {
                            "planned_training_days": "Muss kleiner gleich {} (Dauer des Seminars) sein".format(
                                days
                            )
                        }
                    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            "seminar_detail", kwargs={"slug": self.slug, "year": self.start_date.year}
        )

    def get_admin_change_url(self):
        return reverse("admin:seminars_seminar_change", args=(self.pk,))

    def has_accounting(self):
        fields = [
            "actual_attendees_total",
            "actual_attendence_days_total",
            "actual_funding",
            "actual_training_days",
        ]
        return all(getattr(self, field) is not None for field in fields)

    def get_deadline(self):
        if not self.start_date:
            return None
        year = self.start_date.year
        deadlines = [
            datetime.date(year, 4, 15),
            datetime.date(year, 7, 15),
            datetime.date(year, 10, 15),
            datetime.date(year, 1, 15),
        ]
        return deadlines[get_quarter(self.start_date)]

    def get_max_funding(self):
        if self.start_date:
            year = self.start_date.year
            try:
                fr = FundingRate.objects.get(year=year)
            except FundingRate.DoesNotExist:
                try:
                    fr = FundingRate.objects.get(year=year - 1)
                except FundingRate.DoesNotExist:
                    return None
            return fr.get_max_funding(self)


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
