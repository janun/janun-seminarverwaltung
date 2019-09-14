import datetime

from django.contrib import admin
from django import forms
from django.db import models
from django.db.models import Max, Sum, Avg
from django.utils.html import format_html
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect

import reversion

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportMixin

from backend.users.models import User
from backend.groups.models import JANUNGroup
from backend.utils import format_currency, format_with, admin_link

from .templateddocs import fill_template, FileResponse
from .models import Seminar, SeminarComment
from .filters import QuarterListFilter, YearListFilter, DeadlineFilter, StatusListFilter


class SeminarResource(resources.ModelResource):
    owner = fields.Field(
        column_name="owner", attribute="owner", widget=ForeignKeyWidget(User, "name")
    )

    group = fields.Field(
        column_name="group",
        attribute="group",
        widget=ForeignKeyWidget(JANUNGroup, "name"),
    )

    class Meta:
        model = Seminar


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


class ChangeStatusForm(forms.Form):
    new_status = forms.ChoiceField(label="Neuer Status", choices=Seminar.STATES)


@admin.register(Seminar)
class SeminarAdmin(ImportExportMixin, reversion.admin.VersionAdmin):
    resource_class = SeminarResource
    history_latest_first = True
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
        "get_owner",
        "get_group",
        "training_days",
        "attendees",
        "tnt",
        "funding",
        "tnt_cost",
        "colored_deadline",
    )
    autocomplete_fields = ["owner", "group"]
    # list_editable = ("status",)
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
    change_list_template = "admin/seminars/seminar/change_list.html"
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
            {
                "fields": (
                    "formatted_expense_minus_income",
                    "actual_funding",
                    "advance",
                    "transferred_at",
                )
            },
        ),
        ("Meta", {"fields": ("owner", "created_at", "updated_at")}),
    )

    class Media:
        pass

    def get_changeform_initial_data(self, request):
        get_data = super().get_changeform_initial_data(request)
        get_data["owner"] = request.user
        return get_data

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        if hasattr(response, "context_data") and "cl" in response.context_data:
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

    @admin_link
    def get_group(self, obj):
        return obj.group

    get_group.short_description = Seminar._meta.get_field("group").verbose_name

    @admin_link
    def get_owner(self, obj):
        return obj.owner

    get_owner.short_description = Seminar._meta.get_field("owner").verbose_name

    def formatted_deadline(self, obj):
        return obj.deadline.strftime("%d.%m.%Y")

    formatted_deadline.short_description = "Abrechnungsdeadline"

    def colored_deadline(self, obj):
        color = "transparent"
        if obj.status in ("angemeldet", "zugesagt", "stattgefunden"):
            if obj.deadline <= timezone.now().date():
                color = "red"
            elif obj.deadline - timezone.now().date() < datetime.timedelta(days=14):
                color = "orange"
        return format_html(
            '<span class="small-circle" style="background:{0};"></span> {1}'.format(
                color, obj.deadline.strftime("%d.%m.%Y")
            )
        )

    colored_deadline.short_description = "Abrechnungsdeadline"
    colored_deadline.admin_order_field = "deadline"

    @format_with(format_currency)
    def funding(self, obj):
        return obj.funding

    funding.short_description = "Förderung"
    funding.admin_order_field = "funding"

    def training_days(self, obj):
        return obj.training_days

    training_days.short_description = "Bildungstage"
    training_days.admin_order_field = "training_days"

    def attendees(self, obj):
        return obj.attendees

    attendees.short_description = "TN"
    attendees.admin_order_field = "attendees"

    def tnt(self, obj):
        return obj.tnt

    tnt.short_description = "TNT"
    tnt.admin_order_field = "tnt"

    @format_with(format_currency)
    def tnt_cost(self, obj):
        return obj.tnt_cost

    tnt_cost.short_description = "€/TNT"
    tnt_cost.admin_order_field = "tnt_cost"

    @format_with(format_currency)
    def formatted_income_total(self, obj):
        return obj.income_total

    formatted_income_total.short_description = "Gesamt-Einnahmen"
    formatted_income_total.admin_order_field = "income_total"

    @format_with(format_currency)
    def formatted_expense_total(self, obj):
        return obj.expense_total

    formatted_expense_total.short_description = "Gesamt-Ausgaben"
    formatted_expense_total.admin_order_field = "expense_total"

    @format_with(format_currency)
    def formatted_expense_minus_income(self, obj):
        return obj.expense_minus_income

    formatted_expense_minus_income.short_description = "Ausgaben minus Einnahmen"
    formatted_expense_minus_income.admin_order_field = "expense_minus_income"

    # actions
    # ------------------------------------------------------------------------------

    actions = ["create_proof_of_use", "change_status"]

    def create_proof_of_use(self, request, queryset):
        context = {"seminars": queryset}
        odt_filepath = fill_template("seminars/verwendungsnachweis.odt", context)
        visible_filename = "Verwendungsnachweis.odt"
        return FileResponse(odt_filepath, visible_filename)

    create_proof_of_use.short_description = "Verwendungsnachweis"

    def change_status(self, request, queryset):
        if "new_status" in request.POST:
            form = ChangeStatusForm(request.POST)
            if form.is_valid():
                new_status = form.cleaned_data["new_status"]
                count = queryset.count()
                for seminar in queryset:
                    seminar.status = new_status
                    seminar.save()
                self.message_user(
                    request,
                    "Status auf {0} geändert bei {1} Seminaren".format(
                        new_status, count
                    ),
                )
                return HttpResponseRedirect(request.get_full_path())
        form = ChangeStatusForm()
        return render(
            request,
            "admin/seminars/seminar/change_status.html",
            context={"seminars": queryset, "form": form},
        )

    change_status.short_description = "Status ändern"


# admin.site.register(SeminarComment)
