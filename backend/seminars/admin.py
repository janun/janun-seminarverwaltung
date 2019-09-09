import csv
import datetime

from django.contrib import admin
from django import forms
from django.db import models
from django.http import HttpResponse

from .models import Seminar, SeminarComment


class CommentInlineFormset(forms.BaseInlineFormSet):
    def save_new(self, form, commit=True):
        setattr(form.instance, "owner", self.current_user)  # pylint: disable=no-member
        return super().save_new(form, commit=True)


class CommentsInline(admin.StackedInline):
    model = SeminarComment
    extra = 0
    formset = CommentInlineFormset
    readonly_fields = ("owner", "created_at")

    def has_delete_permission(self, request, obj=None):
        return request.user.has_verwalter_role

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.current_user = request.user
        return formset


class QuarterListFilter(admin.SimpleListFilter):
    title = "Quartal"
    parameter_name = "quarter"

    def lookups(self, request, model_admin):
        return (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_date__quarter=self.value())


class YearListFilter(admin.SimpleListFilter):
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

    def value(self):
        value = super().value()
        if value is None:
            value = str(datetime.date.today().year)
        return value


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    search_fields = ["title", "description", "owner__name", "group__name"]
    save_on_top = True
    inlines = [CommentsInline]
    list_display = (
        "title",
        "start_date",
        "status",
        "owner",
        "group",
        "requested_funding",
        "planned_training_days",
        "planned_attendees_max",
        "tnt",
    )
    autocomplete_fields = ["owner", "group"]
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("owner", "group")
    list_filter = ("status", YearListFilter, QuarterListFilter, "owner", "group")
    formfield_overrides = {
        models.CharField: {"widget": forms.widgets.TextInput(attrs={"size": "100"})}
    }
    fieldsets = (
        ("Allgemeines", {"fields": ("status", "owner", "created_at", "updated_at")}),
        ("Inhalt", {"fields": ("title", "description")}),
        (
            "Zeit & Ort",
            {
                "fields": (
                    "start_date",
                    "start_time",
                    "end_date",
                    "end_time",
                    "location",
                )
            },
        ),
        (
            "Förderung",
            {
                "fields": (
                    "group",
                    "planned_training_days",
                    "planned_attendees_min",
                    "planned_attendees_max",
                    "requested_funding",
                )
            },
        ),
        ("Einnahmen", {"fields": ("income_fees", "income_public", "income_other")}),
        (
            "Ausgaben",
            {
                "fields": (
                    "expense_catering",
                    "expense_accomodation",
                    "expense_referent",
                    "expense_travel",
                    "expense_other",
                )
            },
        ),
        (
            "Abrechnung",
            {
                "fields": (
                    "attendees_total",
                    "attendees_jfg",
                    "attendence_days_total",
                    "attendence_days_jfg",
                    "advance",
                    "training_days",
                    "funding",
                )
            },
        ),
    )

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Ausgewählte als CSV exportieren"


admin.site.register(SeminarComment)
