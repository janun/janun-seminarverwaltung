from django_extensions.db.fields import AutoSlugField

from django.db import models
from django.urls import reverse
from django.db.models import Sum, Count, Case, When, F, ExpressionWrapper, Q
from django.db.models.functions import ExtractYear, Now

from simple_history.models import HistoricalRecords

from backend.utils import slugify_german


class JANUNGroupQuerySet(models.QuerySet):
    def add_annotations(self):
        return self.annotate(
            seminars_this_year=Count(
                "seminars", filter=Q(seminars__start_date__year=ExtractYear(Now()))
            ),
            funding_this_year=Sum(
                Case(
                    When(
                        seminars__actual_funding__isnull=True,
                        then="seminars__requested_funding",
                    ),
                    default="seminars__actual_funding",
                ),
                filter=Q(seminars__start_date__year=ExtractYear(Now())),
            ),
            tnt_this_year=Sum(
                Case(
                    When(
                        seminars__actual_attendence_days_total__isnull=True,
                        then=F("seminars__planned_attendees_max")
                        * F("seminars__planned_training_days"),
                    ),
                    default="seminars__actual_attendence_days_total",
                ),
                filter=Q(seminars__start_date__year=ExtractYear(Now())),
            ),
            tnt_cost_simple_this_year=ExpressionWrapper(
                F("funding_this_year") / F("tnt_this_year"),
                output_field=models.DecimalField(),
            ),
        )


class JANUNGroupManager(models.Manager.from_queryset(JANUNGroupQuerySet)):
    def get_queryset(self):
        return super().get_queryset().add_annotations()


class JANUNGroup(models.Model):
    slug = AutoSlugField(
        "URL-Titel",
        populate_from="name",
        max_length=100,
        unique=True,
        null=True,
        editable=False,
        slugify_function=slugify_german,
    )
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("groups:detail", kwargs={"slug": self.slug})

    objects = JANUNGroupManager()
    history = HistoricalRecords()

    class Meta:
        ordering = ("name",)
        verbose_name = "JANUN-Gruppe"
        verbose_name_plural = "JANUN-Gruppen"
