import datetime

from django.contrib import admin
from django.utils import timezone

from .models import Seminar
from .filter_multiple import MultipleListFilter


class DeadlineFilter(admin.SimpleListFilter):
    title = "Deadline und Status"
    parameter_name = "deadline"

    def lookups(self, request, model_admin):
        return (
            ("expired", "abgelaufen"),
            ("soon_expired", "in 2 Wochen"),
            ("not_soon_expired", "mehr als 2 Wochen hin"),
        )

    def queryset(self, request, queryset):
        if self.value() == "expired":
            return queryset.filter(
                deadline__lte=timezone.now(),
                status__in=("angemeldet", "zugesagt", "stattgefunden"),
            )
        if self.value() == "soon_expired":
            return queryset.filter(
                deadline__lte=timezone.now() + datetime.timedelta(days=14),
                deadline__gt=timezone.now(),
                status__in=("angemeldet", "zugesagt", "stattgefunden"),
            )
        if self.value() == "not_soon_expired":
            return queryset.filter(
                deadline__gt=timezone.now() + datetime.timedelta(days=14)
            )
        return queryset


class StatusListFilter(MultipleListFilter):
    title = "Status"
    parameter_name = "status__in"

    def lookups(self, request, model_admin):
        return Seminar.STATES


class QuarterListFilter(MultipleListFilter):
    title = "Quartal"
    parameter_name = "start_date__quarter__in"

    def lookups(self, request, model_admin):
        return (
            ("1", "1. Quartal"),
            ("2", "2. Quartal"),
            ("3", "3. Quartal"),
            ("4", "4. Quartal"),
        )


class YearListFilter(admin.SimpleListFilter):
    template = "django_admin_listfilter_dropdown/dropdown_filter.html"
    title = "Jahr"
    parameter_name = "year"

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        year_dates = qs.dates("start_date", "year", order="DESC")
        return [(date.year, date.year) for date in year_dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_date__year=int(self.value()))
        return queryset
