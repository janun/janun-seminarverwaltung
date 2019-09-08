from django.contrib import admin


from .models import JANUNGroup


class MembershipInline(admin.StackedInline):
    model = JANUNGroup.members.through  # pylint: disable=no-member
    extra = 0
    verbose_name = "Mitglieder"
    verbose_name_plural = "Mitglieder"
    raw_id_fields = ("user",)


@admin.register(JANUNGroup)
class JANUNGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "members_display", "hats_display")
    inlines = [MembershipInline]

    fieldsets = ((None, {"fields": ("name",)}),)

    def members_display(self, obj):
        return ", ".join([member.name for member in obj.members.all()])

    members_display.short_description = "Mitglieder"

    def hats_display(self, obj):
        return ", ".join([hat.name for hat in obj.group_hats.all()])

    hats_display.short_description = "Hüte"
