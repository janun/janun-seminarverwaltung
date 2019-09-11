import datetime
from admin_auto_filters.filters import AutocompleteFilter as OrigAutocompleteFilter

from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Media, MEDIA_TYPES
from django.contrib import admin
from django.utils import timezone


# Workaround https://github.com/farhan0581/django-admin-autocomplete-filter/issues/16
class AutocompleteFilter(OrigAutocompleteFilter):
    def _add_media(self, model_admin, widget):
        if not hasattr(model_admin, "Media"):
            raise ImproperlyConfigured(
                "Add empty Media class to %s. Sorry about this bug." % model_admin
            )

        def _get_media(obj):
            return Media(media=getattr(obj, "Media", None))

        class FilterMedia:
            js = (
                "admin/js/jquery.init.js",
                "django-admin-autocomplete-filter/js/autocomplete_filter_qs.js",
            )
            css = {
                "screen": ("django-admin-autocomplete-filter/css/autocomplete-fix.css",)
            }

        media = _get_media(model_admin) + widget.media + Media(FilterMedia)

        for name in MEDIA_TYPES:
            setattr(model_admin.Media, name, getattr(media, "_" + name))


class QuarterListFilter(admin.SimpleListFilter):
    template = "django_admin_listfilter_dropdown/dropdown_filter.html"
    title = "Quartal"
    parameter_name = "quarter"

    def lookups(self, request, model_admin):
        return (
            ("1", "1. Quartal"),
            ("2", "2. Quartal"),
            ("3", "3. Quartal"),
            ("4", "4. Quartal"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_date__quarter=self.value())


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


class OwnerFilter(AutocompleteFilter):
    title = "Eigentümer_in"
    field_name = "owner"


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
