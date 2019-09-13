from django.contrib import admin


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
        "seminar_count",
        "actual_tnt_sum",
    )
    inlines = [MembershipInline]
    search_fields = ["name"]

    fieldsets = ((None, {"fields": ("name",)}),)

    def seminar_count(self, obj):
        return obj.seminar_count

    seminar_count.short_description = "# Seminare"
    seminar_count.admin_order_field = "seminar_count"

    def actual_tnt_sum(self, obj):
        return obj.actual_tnt_sum

    actual_tnt_sum.short_description = "TNT"
    actual_tnt_sum.admin_order_field = "actual_tnt_sum"

    def members_display(self, obj):
        return ", ".join([member.name for member in obj.members.all()])

    members_display.short_description = "Mitglieder"

    def hats_display(self, obj):
        return ", ".join([hat.name for hat in obj.group_hats.all()])

    hats_display.short_description = "Hüte"
