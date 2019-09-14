from django.contrib import admin
from django.utils import timezone
from django.db.models import Sum, Avg
from django.template.defaultfilters import floatformat

from .models import JANUNGroup


class MembershipInline(admin.StackedInline):
    model = JANUNGroup.members.through  # pylint: disable=no-member
    extra = 0
    verbose_name = "Mitglieder"
    verbose_name_plural = "Mitglieder"
    autocomplete_fields = ("user",)


@admin.register(JANUNGroup)
class JANUNGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "members_display",
        "hats_display",
        "seminar_count_this_year",
        "tnt_sum_this_year",
        "funding_this_year",
        "tnt_cost_this_year",
    )
    inlines = [MembershipInline]
    search_fields = ["name"]

    fieldsets = ((None, {"fields": ("name",)}),)

    # statistic
    # -----------
    def seminar_count_this_year(self, obj):
        return obj.seminars.this_year().is_confirmed().count()

    seminar_count_this_year.short_description = "Seminare {0}".format(
        timezone.now().year
    )

    def tnt_sum_this_year(self, obj):
        return (
            obj.seminars.this_year()
            .is_confirmed()
            .aggregate(tnt_sum=Sum("tnt"))["tnt_sum"]
        )

    tnt_sum_this_year.short_description = "TNT {0}".format(timezone.now().year)

    def funding_this_year(self, obj):
        return floatformat(
            obj.seminars.this_year()
            .is_confirmed()
            .aggregate(funding_sum=Sum("funding"))["funding_sum"],
            2,
        )

    funding_this_year.short_description = "Förderung {0}".format(timezone.now().year)

    def tnt_cost_this_year(self, obj):
        return floatformat(
            obj.seminars.this_year()
            .is_confirmed()
            .aggregate(tnt_cost_avg=Avg("tnt_cost"))["tnt_cost_avg"],
            2,
        )

    tnt_cost_this_year.short_description = "€/TNT {0}".format(timezone.now().year)

    def members_display(self, obj):
        return ", ".join([member.name for member in obj.members.all()])

    members_display.short_description = "Mitglieder"

    def hats_display(self, obj):
        return ", ".join([hat.name for hat in obj.group_hats.all()])

    hats_display.short_description = "Hüte"
