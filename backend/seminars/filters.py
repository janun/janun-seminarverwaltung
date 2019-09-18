import itertools

from django.contrib import admin

from .models import Seminar
from .filter_multiple import MultipleListFilter
from .states import STATES_CONFIRMED


class DeadlineFilter(admin.SimpleListFilter):
    title = "Deadline"
    parameter_name = "deadline"

    def lookups(self, request, model_admin):
        return (
            ("expired", "abgelaufen"),
            ("soon", "in 2 Wochen"),
            ("not_soon", "mehr als 2 Wochen hin"),
            ("not_applicable", "Nicht mehr anwendbar"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(deadline_status=self.value())
        return queryset


class StatusListFilter(MultipleListFilter):
    title = "Status"
    parameter_name = "status__in"

    def lookups(self, request, model_admin):
        return Seminar.STATE_CHOICES

    def choices(self, changelist):
        choices = super().choices(changelist)
        all_confirmed_option = {
            "selected": self.value() == ",".join(STATES_CONFIRMED),
            "query_string": changelist.get_query_string(
                {self.parameter_name: ",".join(STATES_CONFIRMED)}
            ),
            "display": "Alle zugesagten",
            "reset": True,
        }
        choices = itertools.chain(choices, [all_confirmed_option])
        return choices


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
