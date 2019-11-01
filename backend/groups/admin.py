from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse

from import_export.admin import ImportExportMixin

from backend.utils import format_currency, format_number, format_with

from .models import JANUNGroup
from .resources import JANUNGroupResource


class MembershipInline(admin.StackedInline):
    model = JANUNGroup.members.through  # pylint: disable=no-member
    extra = 0
    verbose_name = "Mitglied"
    verbose_name_plural = "Mitglieder"


class GroupHatInline(admin.StackedInline):
    model = JANUNGroup.group_hats.through  # pylint: disable=no-member
    extra = 0
    verbose_name = "Gruppen-Hut"
    verbose_name_plural = "Gruppen-Hüte"


@admin.register(JANUNGroup)
class JANUNGroupAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = JANUNGroupResource
    list_display = (
        "name",
        "members_display",
        "hats_display",
        "seminar_count_this_year",
        "tnt_this_year",
        "funding_this_year",
        "tnt_cost_this_year",
    )
    inlines = [MembershipInline, GroupHatInline]
    search_fields = ["name"]

    fieldsets = ((None, {"fields": ("name",)}),)

    # statistic getters
    # -----------------------
    def seminar_count_this_year(self, obj):
        url = reverse(
            "admin:seminars_seminar_changelist"
        ) + "?group__id__exact={0}&year={1}".format(obj.pk, timezone.now().year)

        return format_html('<a href="{0}">{1}</a>'.format(url, obj.seminars_this_year))

    seminar_count_this_year.short_description = "# Seminare {0}".format(
        timezone.now().year
    )
    seminar_count_this_year.admin_order_field = "seminars_this_year"

    @format_with(format_number)
    def tnt_this_year(self, obj):
        return obj.tnt_this_year

    tnt_this_year.short_description = "∑ TNT {0}".format(timezone.now().year)
    tnt_this_year.admin_order_field = "tnt_this_year"

    @format_with(format_currency)
    def funding_this_year(self, obj):
        return obj.funding_this_year

    funding_this_year.short_description = "∑ Förderung {0}".format(timezone.now().year)
    funding_this_year.admin_order_field = "funding_this_year"

    @format_with(format_currency)
    def tnt_cost_this_year(self, obj):
        return obj.tnt_cost_simple_this_year

    tnt_cost_this_year.short_description = "Förderung/TNT {0}".format(
        timezone.now().year
    )
    tnt_cost_this_year.admin_order_field = "tnt_cost_simple_this_year"

    def members_display(self, obj):
        return ", ".join([member.name for member in obj.members.all()])

    members_display.short_description = "Mitglieder"

    def hats_display(self, obj):
        return ", ".join([hat.name for hat in obj.group_hats.all()])

    hats_display.short_description = "Hüte"
