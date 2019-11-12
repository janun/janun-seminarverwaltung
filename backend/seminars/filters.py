import itertools

from django.contrib import admin
from django import forms

import django_filters

from backend.groups.models import JANUNGroup
from backend.users.models import User

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


class SearchInput(forms.TextInput):
    template_name = "widgets/search_input.html"


class SeminarStaffFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label="Filter nach Titel",
        lookup_expr="icontains",
        widget=SearchInput(attrs={"autofocus": True}),
    )
    quarter = django_filters.ChoiceFilter(
        label="Quartal",
        field_name="start_date",
        lookup_expr="quarter",
        choices=[(i, "{0}".format(i)) for i in range(1, 5)],
    )
    deadline = django_filters.ChoiceFilter(
        label="Abrechnungsfrist",
        field_name="deadline_status",
        choices=(
            ("expired", "abgelaufen"),
            ("soon", "in 14 Tagen"),
            ("not_soon", "länger hin"),
            ("not_applicable", "nicht zutreffend"),
        ),
    )
    status = django_filters.ChoiceFilter(choices=Seminar.STATE_CHOICES)
    group = django_filters.ModelChoiceFilter(
        null_label="keine", queryset=JANUNGroup.objects.order_by("name").all()
    )
    owner = django_filters.ModelChoiceFilter(
        label="Besitzer_in", queryset=User.objects.order_by("name").all()
    )

    class Meta:
        model = Seminar
        fields = ["title", "quarter", "deadline", "status", "group", "owner"]
