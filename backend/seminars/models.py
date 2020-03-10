import datetime
from decimal import Decimal
from typing import Optional
from model_utils import Choices
from django_extensions.db.fields import AutoSlugField
import formulas
from formulas.errors import FormulaError

from django.db import models
from django.db.models import Case, When, F, ExpressionWrapper, Value, Q, Sum, Count
from django.db.models.functions import ExtractYear, Concat, Cast, Coalesce
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.template import defaultfilters

from simple_history.models import HistoricalRecords

from backend.users.models import User
from backend.groups.models import JANUNGroup
from backend.utils import slugify_german
from backend.dashboard.history import BaseHistoricalModel

from .states import (
    STATES_CONFIRMED,
    STATES_REJECTED,
    STATES,
    STATES_PROGRESS,
    STATES_BILLS_PRESENT,
)


def get_quarter(date: datetime.date) -> int:
    return (date.month - 1) // 3


def add_none(*p) -> Optional[Decimal]:
    """treat None values as 0, return None if all args are None"""
    if all(v is None for v in p):
        return None
    return sum(filter(None, p))


class FundingRate(models.Model):
    year = models.IntegerField("Jahr", unique=True)

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
        help_text="engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450) mit B = Anzahl der Bildungstage",
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
        help_text="engl. Excel-Formel, z.B. =IF(B>=3,(B-3)*200+450,450) mit B = Anzahl der Bildungstage",
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
                raise ValidationError({"single_limit_formula": str(error)})

        if self.group_limit_formula:
            try:
                self.test_formula(self.group_limit_formula)
            except FormulaError as error:
                raise ValidationError({"group_limit_formula": str(error)})

    def get_rate(self, has_group: bool, days: int) -> Decimal:
        if has_group:
            if days == 1 and self.group_rate_one_day:
                return self.group_rate_one_day
            return self.group_rate
        if days == 1 and self.single_rate_one_day:
            return self.single_rate_one_day
        return self.single_rate

    def limit(
        self, group, planned_training_days, planned_attendees_max, funding: Decimal
    ) -> Decimal:
        upper_limit = self.group_limit if group else self.single_limit
        if upper_limit and funding > upper_limit:
            funding = upper_limit

        formula = self.group_limit_formula if group else self.single_limit_formula
        if formula:
            lower_limit = float(
                formulas.Parser().ast(formula)[1].compile()(B=planned_training_days)
            )
            if lower_limit and funding > lower_limit:
                funding = lower_limit

        return funding

    def get_max_funding(
        self, group, planned_training_days, planned_attendees_max
    ) -> Decimal:
        if planned_training_days and planned_attendees_max:
            rate = self.get_rate(group, planned_training_days)
            tnt = planned_training_days * planned_attendees_max
            funding = rate * tnt
            return self.limit(
                group, planned_training_days, planned_attendees_max, funding
            )

    def __str__(self) -> str:
        return "Förderungssätze %s" % self.year

    history = HistoricalRecords(bases=[BaseHistoricalModel])

    def get_absolute_url(self) -> str:
        return reverse("config:funding_update", kwargs={"year": self.year})

    class Meta:
        verbose_name = "Förderungssatz"
        verbose_name_plural = "Förderungssätze"


class SeminarQuerySet(models.QuerySet):
    def annotate_planned_attendence_days(self) -> models.QuerySet:
        return self.annotate(
            planned_attendence_days=F("planned_attendees_max")
            * F("planned_training_days")
        )

    def annotate_year(self) -> models.QuerySet:
        return self.annotate(year=ExtractYear("start_date"))

    def annotate_deadline(self) -> models.QuerySet:
        return self.annotate_year().annotate(
            deadline=Case(
                When(
                    start_date__quarter=1,
                    then=Cast(
                        Concat(Cast("year", models.TextField()), Value("-04-15")),
                        models.DateField(),
                    ),
                ),
                When(
                    start_date__quarter=2,
                    then=Cast(
                        Concat(Cast("year", models.TextField()), Value("-07-15")),
                        models.DateField(),
                    ),
                ),
                When(
                    start_date__quarter=3,
                    then=Cast(
                        Concat(Cast("year", models.TextField()), Value("-10-15")),
                        models.DateField(),
                    ),
                ),
                When(
                    start_date__quarter=4,
                    then=Cast(
                        Concat(
                            Cast(F("year") + 1, models.TextField()), Value("-01-15")
                        ),
                        models.DateField(),
                    ),
                ),
                output_field=models.DateField(),
            )
        )

    def annotate_deadline_applicable(self) -> models.QuerySet:
        return self.annotate(
            deadline_applicable=Case(
                When(status__in=("angemeldet", "zugesagt", "stattgefunden"), then=True),
                default=False,
                output_field=models.BooleanField(),
            )
        )

    def annotate_funding(self) -> models.QuerySet:
        return self.annotate(
            funding=Case(
                When(actual_funding__isnull=True, then="requested_funding"),
                default="actual_funding",
            )
        )

    def annotate_tnt(self) -> models.QuerySet:
        return self.annotate_planned_attendence_days().annotate(
            tnt=Case(
                When(
                    actual_attendence_days_total__isnull=True,
                    then="planned_attendence_days",
                ),
                default="actual_attendence_days_total",
            )
        )

    def annotate_tnt_cost(self) -> models.QuerySet:
        return (
            self.annotate_tnt()
            .annotate_funding()
            .annotate(
                tnt_cost=Case(
                    When(
                        tnt__gt=Value(0),
                        then=ExpressionWrapper(
                            F("funding") / F("tnt"), output_field=models.DecimalField()
                        ),
                    ),
                    default=Value(None),
                )
            )
        )

    def annotate_attendees(self) -> models.QuerySet:
        return self.annotate(
            attendees=Case(
                When(actual_attendees_total__isnull=True, then="planned_attendees_max"),
                default="actual_attendees_total",
            )
        )

    def annotate_training_days(self) -> models.QuerySet:
        return self.annotate(
            training_days=Case(
                When(actual_training_days__isnull=True, then="planned_training_days"),
                default="actual_training_days",
            )
        )

    def annotate_income_total(self) -> models.QuerySet:
        return self.annotate(
            income_total=Coalesce("income_fees", 0)
            + Coalesce("income_public", 0)
            + Coalesce("income_other", 0)
        )

    def annotate_expense_total(self) -> models.QuerySet:
        return self.annotate(
            expense_total=Coalesce("expense_accomodation", 0)
            + Coalesce("expense_catering", 0)
            + Coalesce("expense_other", 0)
            + Coalesce("expense_referent", 0)
            + Coalesce("expense_travel", 0)
        )

    def annotate_expense_minus_income(self) -> models.QuerySet:
        return self.annotate_income_total().annotate_expense_total.annotate(
            expense_minus_income=Coalesce("expense_total", 0)
            - Coalesce("income_total", 0)
        )

    def annotate_deadline_status(self) -> models.QuerySet:
        return (
            self.annotate_deadline_applicable()
            .annotate_deadline()
            .annotate(
                deadline_status=Case(
                    When(
                        Q(deadline_applicable=True) & Q(deadline__lte=timezone.now()),
                        then=Value("expired"),
                    ),
                    When(
                        Q(deadline_applicable=True)
                        & Q(deadline__lte=timezone.now() + datetime.timedelta(days=14)),
                        then=Value("soon"),
                    ),
                    When(
                        Q(deadline_applicable=True)
                        & Q(deadline__gt=timezone.now() + datetime.timedelta(days=14)),
                        then=Value("not_soon"),
                    ),
                    When(deadline_applicable=False, then=Value("not_applicable")),
                    default=Value("unknown"),
                    output_field=models.CharField(),
                )
            )
        )

    def is_confirmed(self) -> models.QuerySet:
        return self.filter(status__in=(STATES_CONFIRMED))

    def is_rejected(self) -> models.QuerySet:
        return self.filter(status__in=(STATES_REJECTED))

    def is_not_rejected(self) -> models.QuerySet:
        return self.exclude(status__in=(STATES_REJECTED))

    def is_in_progress(self) -> models.QuerySet:
        return self.filter(status__in=(STATES_PROGRESS))

    def is_bills_present(self) -> models.QuerySet:
        return self.filter(status__in=(STATES_BILLS_PRESENT))

    def last_year(self) -> models.QuerySet:
        return self.filter(start_date__year=timezone.now().year - 1)

    def this_year(self) -> models.QuerySet:
        return self.filter(start_date__year=timezone.now().year)

    def next_year(self) -> models.QuerySet:
        return self.filter(start_date__year=timezone.now().year + 1)

    def get_aggregates(self) -> dict:
        return (
            self.annotate_funding()
            .annotate_tnt()
            .aggregate(
                count=Count("pk"), funding_sum=Sum("funding"), tnt_sum=Sum("tnt")
            )
        )


class SeminarManager(models.Manager.from_queryset(SeminarQuerySet)):
    pass


class Seminar(models.Model):
    STATE_CHOICES = Choices(*STATES)

    title = models.CharField("Titel", max_length=255, db_index=True)
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
        verbose_name="Besitzer_in",
    )
    group = models.ForeignKey(
        JANUNGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seminars",
        verbose_name="JANUN-Gruppe",
    )
    description = models.TextField(
        "Beschreibung",
        help_text="Um was genau geht es in dem Seminar? Welche Inhalte werden vermittelt?",
        blank=True,
    )
    start_date = models.DateField(
        "Start-Datum", help_text="z.B. 2.5.2019", db_index=True
    )
    start_time = models.TimeField(
        "Start-Zeit", help_text="z.B. 15:00", blank=True, null=True
    )
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
        "tatsächliche Bildungstage", blank=True, null=True
    )
    actual_funding = models.DecimalField(
        "tatsächlicher Förderbedarf",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    transferred_at = models.DateField("überwiesen am", blank=True, null=True)
    expense_catering = models.DecimalField(
        "Verpflegung", max_digits=10, decimal_places=2, blank=True, null=True
    )
    expense_accomodation = models.DecimalField(
        "Unterkunft", max_digits=10, decimal_places=2, blank=True, null=True
    )

    def get_expense_accomodation_and_catering(self) -> Optional[Decimal]:
        return add_none(self.expense_catering, self.expense_accomodation)

    get_expense_accomodation_and_catering.short_description = (
        "Ausgaben für Unterkunft und Verpflegung"
    )
    expense_accomodation_and_catering = property(get_expense_accomodation_and_catering)

    expense_referent = models.DecimalField(
        "Referent_innen", max_digits=10, decimal_places=2, blank=True, null=True
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
    confirmed_at = models.DateTimeField("Zugesagt am", null=True, blank=True)

    class Meta:
        ordering = ("-start_date",)
        verbose_name = "Seminar"
        verbose_name_plural = "Seminare"

    objects = SeminarManager()
    history = HistoricalRecords(
        excluded_fields=["updated_at", "slug"], bases=[BaseHistoricalModel]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        # in case of changed status:
        if self.__original_status != self.status:
            if self.status == "zugesagt":
                self.confirmed_at = timezone.now()

        super().save(*args, **kwargs)
        self.__original_status = self.status

    def clean(self):
        errors = {}
        # validate planned_attendees_min/max
        if self.planned_attendees_min and self.planned_attendees_max:
            if self.planned_attendees_min > self.planned_attendees_max:
                errors["planned_attendees_max"] = "Muss größer/gleich Minimal-Wert sein"
        if self.end_date and self.start_date:
            # validate end_date, start_date
            if self.end_date < self.start_date:
                errors["end_date"] = "Muss größer/gleich Start-Datum sein"
            # validate end_time, start_time
            if self.end_date == self.start_date and self.start_time and self.end_time:
                if self.end_time < self.start_time:
                    errors["end_time"] = "Muss größer/gleich Start-Zeit sein"
            # validate planned_training_days
            if self.planned_training_days:
                days = (self.end_date - self.start_date).days + 1
                if self.planned_training_days > days:
                    errors[
                        "planned_training_days"
                    ] = "Muss kleiner gleich {} (Dauer des Seminars) sein".format(days)
        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return "{}, {}".format(
            self.title, defaultfilters.date(self.start_date, "d.m.y")
        )

    def get_absolute_url(self) -> str:
        return reverse(
            "seminars:detail", kwargs={"slug": self.slug, "year": self.start_date.year}
        )

    def get_admin_change_url(self):
        return reverse("admin:seminars_seminar_change", args=(self.pk,))

    def has_accounting(self) -> bool:
        fields = [
            "actual_attendees_total",
            "actual_attendence_days_total",
            "actual_funding",
            "actual_training_days",
        ]
        return all(getattr(self, field) is not None for field in fields)

    def get_deadline(self) -> datetime.date:
        if not self.start_date:
            return None
        year = self.start_date.year
        deadlines = [
            datetime.date(year, 4, 15),
            datetime.date(year, 7, 15),
            datetime.date(year, 10, 15),
            datetime.date(year + 1, 1, 15),
        ]
        return deadlines[get_quarter(self.start_date)]

    def get_max_funding(self) -> Optional[Decimal]:
        if self.start_date:
            year = self.start_date.year
            return get_max_funding(
                year, self.group, self.planned_training_days, self.planned_attendees_max
            )


def get_max_funding(
    year, group, planned_training_days, planned_attendees_max
) -> Optional[Decimal]:
    try:
        fr = FundingRate.objects.get(year=year)
    except FundingRate.DoesNotExist:
        try:
            fr = FundingRate.objects.get(year=year - 1)
        except FundingRate.DoesNotExist:
            return None
    return fr.get_max_funding(group, planned_training_days, planned_attendees_max)


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
    def was_edited(self) -> bool:
        return self.updated_at - self.created_at > datetime.timedelta(seconds=1)

    def get_absolute_url(self) -> str:
        return "{}#comments".format(self.seminar.get_absolute_url())

    history = HistoricalRecords(
        excluded_fields=["updated_at"], bases=[BaseHistoricalModel]
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"

    def __str__(self) -> str:
        return "Kommentar an {}".format(self.seminar)


class SeminarView(models.Model):
    """save who viewed the seminar and when"""

    when = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="+"
    )
    seminar = models.ForeignKey(
        Seminar, on_delete=models.CASCADE, null=True, blank=True, related_name="views"
    )

    def __str__(self) -> str:
        return "{} besuchte {} am {}".format(self.user, self.seminar, self.when)
