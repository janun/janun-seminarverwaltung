from decimal import InvalidOperation

from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django import forms
from django.db import models
from django.db.models import Max, Sum, Avg, Count
from django.utils.html import format_html
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from import_export.admin import ImportExportMixin

from backend.users.models import User
from backend.groups.models import JANUNGroup
from backend.utils import format_currency, format_with, admin_link, median_value

from .templateddocs import fill_template, FileResponse
from .models import Seminar, SeminarComment, FundingRate
from .filters import QuarterListFilter, YearListFilter, DeadlineFilter, StatusListFilter
from .resources import SeminarResource


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
    new_status = forms.ChoiceField(label="Neuer Status", choices=Seminar.STATE_CHOICES)


@admin.register(FundingRate)
class FundingRateAdmin(admin.ModelAdmin):
    list_display = ("year", "group_rate", "single_rate")
    fieldsets = (
        (None, {"fields": ("year",)}),
        (
            "Gruppen",
            {
                "fields": (
                    "group_rate",
                    "group_rate_one_day",
                    "group_limit_formula",
                    "group_limit",
                )
            },
        ),
        (
            "Einzelpersonen",
            {
                "fields": (
                    "single_rate",
                    "single_rate_one_day",
                    "single_limit_formula",
                    "single_limit",
                )
            },
        ),
    )


@admin.register(Seminar)
class SeminarAdmin(ImportExportMixin, admin.ModelAdmin):
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
        "planned_attendence_days",
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
            "Anmeldung - Förderung",
            {
                "fields": (
                    "group",
                    "planned_training_days",
                    "planned_attendees_min",
                    "planned_attendees_max",
                    "requested_funding",
                    "planned_attendence_days",
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
            filtered_query_set = response.context_data["cl"].queryset
            extra_context = {}

            # stat for this year
            this_year_confirmed = (
                Seminar.objects.this_year()
                .is_confirmed()
                .aggregate(
                    count=Count("pk"), funding_sum=Sum("funding"), tnt_sum=Sum("tnt")
                )
            )
            extra_context["this_year_confirmed"] = this_year_confirmed

            # stat for filtered_query_set
            stats = filtered_query_set.aggregate(
                count=Count("pk"), funding_sum=Sum("funding"), tnt_sum=Sum("tnt")
            )
            response.context_data["cl"].stats = stats

            response.context_data.update(extra_context)
        return response

    # formatted_fields and accessors to annotated values
    # ------------------------------------------------------------------------------

    @admin_link
    def get_group(self, obj):
        return obj.group

    get_group.short_description = Seminar._meta.get_field("group").verbose_name

    def planned_attendence_days(self, obj):
        return obj.planned_attendence_days

    planned_attendence_days.short_description = "Geplante TNT"
    planned_attendence_days.admin_order_field = "planned_attendence_days"

    @admin_link
    def get_owner(self, obj):
        return obj.owner

    get_owner.short_description = Seminar._meta.get_field("owner").verbose_name

    def formatted_deadline(self, obj):
        return obj.deadline.strftime("%d.%m.%Y")

    formatted_deadline.short_description = "Abrechnungsdeadline"

    def colored_deadline(self, obj):
        color = "transparent"
        if obj.deadline_status == "soon":
            color = "yellow"
        if obj.deadline_status == "expired":
            color = "red"
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

    actions = ["create_proof_of_use", "change_status", "list_selected"]

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

    def list_selected(self, request, queryset):
        id_list = queryset.values_list("id", flat=True)
        id_str = ",".join(str(x) for x in id_list)
        return HttpResponseRedirect(request.path + "?id__in=" + id_str)

    list_selected.short_description = "Nur ausgewählte anzeigen"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("stats/", self.admin_site.admin_view(self.stats))]
        return my_urls + urls

    def stats(self, request):
        context = dict(self.admin_site.each_context(request))
        queryset = Seminar.objects.this_year().is_confirmed().order_by("start_date")
        extra_context = queryset.aggregate(
            count=Count("pk"),
            funding_sum=Sum("funding"),
            funding_avg=Avg("funding"),
            funding_max=Max("funding"),
            tnt_sum=Sum("tnt"),
            tnt_avg=Avg("tnt"),
            tnt_max=Max("tnt"),
            tnt_cost_avg=Avg("tnt_cost"),
            tnt_cost_max=Max("tnt_cost"),
        )
        try:
            extra_context["tnt_cost"] = (
                extra_context["funding_sum"] // extra_context["tnt_sum"]
            )
        except TypeError:
            pass
        except InvalidOperation:
            pass
        extra_context["funding_median"] = median_value(queryset, "funding")
        extra_context["tnt_median"] = median_value(queryset, "tnt")
        extra_context["tnt_cost_median"] = median_value(queryset, "tnt_cost")
        status_list = (
            "zugesagt",
            "stattgefunden",
            "Abrechnung abgeschickt",
            "Abrechnung angekommen",
            "rechnerische Prüfung",
            "inhaltliche Prüfung",
            "Zweitprüfung",
            "fertig geprüft",
            "überwiesen",
        )
        extra_context["queryset_url"] = reverse(
            "admin:seminars_seminar_changelist"
        ) + "?year={0}&status__in={1}".format(
            timezone.now().year, ",".join(status_list)
        )
        extra_context["seminars"] = queryset
        extra_context["groups"] = JANUNGroup.objects.all()
        context.update(extra_context)

        return TemplateResponse(request, "admin/seminars/seminar/stats.html", context)


# admin.site.register(SeminarComment)
