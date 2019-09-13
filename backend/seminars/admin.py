import csv

from django.contrib import admin
from django import forms
from django.db import models
from django.db.models import Max, Sum, Avg
from django.http import HttpResponse
from django.template.defaultfilters import floatformat

from reversion.admin import VersionAdmin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .templateddocs import fill_template, FileResponse
from .models import Seminar, SeminarComment
from .filters import QuarterListFilter, YearListFilter, DeadlineFilter, StatusListFilter


class CommentInlineFormset(forms.BaseInlineFormSet):
    def save_new(self, form, commit=True):
        setattr(form.instance, "owner", self.current_user)  # pylint: disable=no-member
        return super().save_new(form, commit=True)


class CommentsInline(admin.StackedInline):
    model = SeminarComment
    extra = 1
    formset = CommentInlineFormset
    readonly_fields = ("owner", "created_at")

    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user == obj.owner
        return False

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.current_user = request.user
        return formset


@admin.register(Seminar)
class SeminarAdmin(VersionAdmin):
    search_fields = [
        "title",
        "description",
        "owner__name",
        "owner__username",
        "group__name",
    ]
    save_on_top = True
    inlines = [CommentsInline]
    list_display = (
        "title",
        "start_date",
        "status",
        "owner",
        "group",
        "training_days",
        "attendees",
        "tnt",
        "formatted_funding",
        "deadline",
    )
    autocomplete_fields = ["owner", "group"]
    list_editable = ("status",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "formatted_deadline",
        "formatted_income_total",
        "formatted_expense_total",
        "formatted_expense_minus_income",
    )
    list_select_related = ("owner", "group")
    list_filter = (
        YearListFilter,
        QuarterListFilter,
        StatusListFilter,
        ("owner", RelatedDropdownFilter),
        ("group", RelatedDropdownFilter),
        DeadlineFilter,
    )
    formfield_overrides = {
        models.CharField: {"widget": forms.widgets.TextInput(attrs={"size": "100"})}
    }
    fieldsets = (
        (None, {"fields": ("status",)}),
        ("Inhalt", {"fields": ("title", "description")}),
        (
            "Zeit & Ort",
            {
                "fields": (
                    "start_date",
                    "start_time",
                    "end_date",
                    "end_time",
                    "formatted_deadline",
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
            "Abrechnung - TNT",
            {
                "fields": (
                    "actual_attendees_total",
                    "actual_attendees_jfg",
                    "actual_training_days",
                    "actual_attendence_days_total",
                    "actual_attendence_days_jfg",
                )
            },
        ),
        (
            "Abrechnung - Ausgaben",
            {
                "classes": ("js-sum",),
                "fields": (
                    "expense_catering",
                    "expense_accomodation",
                    "expense_referent",
                    "expense_travel",
                    "expense_other",
                    "formatted_expense_total",
                ),
            },
        ),
        (
            "Abrechnung - Einnahmen",
            {
                "classes": ("js-sum",),
                "fields": (
                    "income_fees",
                    "income_public",
                    "income_other",
                    "formatted_income_total",
                ),
            },
        ),
        (
            "Abrechnung - Bilanz",
            {"fields": ("formatted_expense_minus_income", "actual_funding", "advance")},
        ),
        ("Meta", {"fields": ("owner", "created_at", "updated_at")}),
    )

    class Media:
        pass

    actions = ["export_as_csv", "create_proof_of_use"]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, "context_data"):
            queryset = response.context_data["cl"].queryset
            extra_context = queryset.aggregate(
                funding_sum=Sum("funding"),
                funding_avg=Avg("funding"),
                funding_max=Max("funding"),
                tnt_sum=Sum("tnt"),
                tnt_avg=Avg("tnt"),
                tnt_max=Max("tnt"),
                tnt_cost_avg=Avg("tnt_cost"),
                tnt_cost_max=Max("tnt_cost"),
                attendees_sum=Sum("attendees"),
                attendees_avg=Avg("attendees"),
                attendees_max=Max("attendees"),
                training_days_sum=Sum("training_days"),
                training_days_avg=Avg("training_days"),
                training_days_max=Max("training_days"),
            )
            response.context_data.update(extra_context)
        return response

    # formatted_fields and accessors to annotated values
    # ------------------------------------------------------------------------------

    def formatted_deadline(self, obj):
        return obj.deadline.strftime("%d.%m.%Y")

    formatted_deadline.short_description = "Abrechnungsdeadline"

    def formatted_funding(self, obj):
        return floatformat(obj.funding, 2)

    formatted_funding.short_description = "Förderung"
    formatted_funding.admin_order_field = "funding"

    def training_days(self, obj):
        return obj.training_days

    training_days.short_description = "Bildungstage"
    training_days.admin_order_field = "traning_days"

    def attendees(self, obj):
        return obj.attendees

    attendees.short_description = "TN"
    attendees.admin_order_field = "attendees"

    def tnt(self, obj):
        return obj.tnt

    tnt.short_description = "TNT"
    tnt.admin_order_field = "tnt"

    def formatted_income_total(self, obj):
        return floatformat(obj.income_total, 2)

    formatted_income_total.short_description = "Gesamt-Einnahmen"
    formatted_income_total.admin_order_field = "income_total"

    def formatted_expense_total(self, obj):
        return floatformat(obj.expense_total, 2)

    formatted_expense_total.short_description = "Gesamt-Ausgaben"
    formatted_expense_total.admin_order_field = "expense_total"

    def formatted_expense_minus_income(self, obj):
        return floatformat(obj.expense_minus_income, 2)

    formatted_expense_minus_income.short_description = "Ausgaben minus Einnahmen"
    formatted_expense_minus_income.admin_order_field = "expense_minus_income"

    # actions
    # ------------------------------------------------------------------------------

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        field_verbose_names = [field.verbose_name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)
        writer.writerow(field_verbose_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Ausgewählte als CSV exportieren"

    def create_proof_of_use(self, request, queryset):
        context = {"seminars": queryset}
        odt_filepath = fill_template("seminars/verwendungsnachweis.odt", context)
        visible_filename = "Verwendungsnachweis.odt"
        return FileResponse(odt_filepath, visible_filename)

    create_proof_of_use.short_description = (
        "Ausgewählte als Verwendungsnachweis exportieren"
    )


# admin.site.register(SeminarComment)
