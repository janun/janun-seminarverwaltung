import csv

from django.contrib import admin
from django import forms
from django.db import models
from django.http import HttpResponse

from .models import Seminar, SeminarComment, SeminarIncomeRecord, SeminarExpenseRecord


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


class IncomeFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        kwargs["initial"] = [
            {"amount": "0.0", "name": "TN-Beiträge"},
            {"amount": "0.0", "name": "Öffentliche Zuwendungen"},
            {"amount": "0.0", "name": "Sonstiges"},
        ]
        super().__init__(*args, **kwargs)


class ExpenseFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        kwargs["initial"] = [
            {"amount": "0.0", "name": "Verpflegung"},
            {"amount": "0.0", "name": "Unterkunft"},
            {"amount": "0.0", "name": "Referent_innen"},
            {"amount": "0.0", "name": "Fahrtkosten"},
            {"amount": "0.0", "name": "Sonstiges"},
        ]

        super().__init__(*args, **kwargs)


class IncomeInline(admin.TabularInline):
    model = SeminarIncomeRecord
    extra = 3
    max_num = 3
    formset = IncomeFormSet


class ExpenseInline(admin.TabularInline):
    model = SeminarExpenseRecord
    extra = 5
    max_num = 5
    formset = ExpenseFormSet


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
            return queryset.by_year(int(self.value()))
        return queryset


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    search_fields = ["title", "description", "owner__name", "group__name"]
    save_on_top = True
    inlines = [ExpenseInline, IncomeInline, CommentsInline]
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
    list_select_related = ("owner", "group")
    list_filter = ("status", YearListFilter, QuarterListFilter, "owner", "group")
    formfield_overrides = {
        models.CharField: {"widget": forms.widgets.TextInput(attrs={"size": "100"})}
    }
    fieldsets = (
        ("Status", {"fields": ("status",)}),
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
