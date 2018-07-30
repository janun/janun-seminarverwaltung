from django.contrib import admin

from .models import JANUNGroup


# class MembershipInline(admin.TabularInline):
#     model = JANUNGroup.members.through

@admin.register(JANUNGroup)
class JANUNGroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'get_members']
    # filter_horizontal = ['members']
    # inlines = [
    #     MembershipInline,
    # ]

    def get_members(self, obj):
        members = list(obj.members.all()) + list(obj.group_hats.all())
        return "\n".join([m.name for m in members])
    get_members.short_description = 'Mitglieder'
