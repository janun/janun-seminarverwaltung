import csv

from django.contrib import admin
from django import forms
from django.db import models
from django.http import HttpResponse

from django_admin_listfilter_dropdown.filters import (
    ChoiceDropdownFilter,
    RelatedDropdownFilter,
)

from .templateddocs import fill_template, FileResponse
from .models import Seminar, SeminarComment
from .filters import QuarterListFilter, YearListFilter, OwnerFilter


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
        return request.user.has_verwalter_role or request.user == obj.owner

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.current_user = request.user
        return formset


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
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
        "funding",
        "training_days",
        "attendees",
        "tnt",
    )
    autocomplete_fields = ["owner", "group"]
    list_editable = ("status",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "formatted_deadline",
        "income_total",
        "expense_total",
    )
    list_select_related = ("owner", "group")
    list_filter = (
        ("status", ChoiceDropdownFilter),
        YearListFilter,
        QuarterListFilter,
        OwnerFilter,
        ("group", RelatedDropdownFilter),
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
            "Abrechnung",
            {
                "fields": (
                    "actual_attendees_total",
                    "actual_attendees_jfg",
                    "actual_attendence_days_total",
                    "actual_attendence_days_jfg",
                    "actual_training_days",
                    "advance",
                    "actual_funding",
                )
            },
        ),
        (
            "Abrechnung - Einnahmen",
            {
                "fields": (
                    "income_fees",
                    "income_public",
                    "income_other",
                    "income_total",
                )
            },
        ),
        (
            "Abrechnung - Ausgaben",
            {
                "fields": (
                    "expense_catering",
                    "expense_accomodation",
                    "expense_referent",
                    "expense_travel",
                    "expense_other",
                    "expense_total",
                )
            },
        ),
        ("Meta", {"fields": ("owner", "created_at", "updated_at")}),
    )

    actions = ["export_as_csv", "create_proof_of_use"]

    class Media:
        pass

    # # restrict status choices
    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     if db_field.name == "status":
    #         # kwargs['choices'] = get_next_states()
    #         print(db_field.value)
    #     return super().formfield_for_choice_field(db_field, request, **kwargs)

    def formatted_deadline(self, obj):
        return obj.deadline.strftime("%d.%m.%Y")

    formatted_deadline.short_description = "Abrechnungsdeadline"

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

    def create_proof_of_use(self, request, queryset):
        context = {"seminars": queryset}
        odt_filepath = fill_template("seminars/verwendungsnachweis.odt", context)
        visible_filename = "Verwendungsnachweis.odt"
        return FileResponse(odt_filepath, visible_filename)

    create_proof_of_use.short_description = (
        "Ausgewählte als Verwendungsnachweis exportieren"
    )


admin.site.register(SeminarComment)
