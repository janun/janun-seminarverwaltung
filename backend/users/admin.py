from django.contrib import admin
from django.contrib.auth.models import Group

# from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.account.models import EmailAddress

from .models import User

# remove unused apps from admin
admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)

# enforce normal login for admin login
# admin.site.login = login_required(admin.site.login)
admin.site.site_header = "JANUN Seminare Verwaltung"
admin.site.site_title = "JANUN Seminare Verwaltung"
admin.site.index_title = "JANUN Seminare Verwaltung"


class UserAdmin(BaseUserAdmin):
    search_fields = ["username", "name"]
    list_display = (
        "username",
        "name",
        "role",
        "janun_groups_display",
        "group_hats_display",
    )
    readonly_fields = ("last_login", "date_joined", "updated_at")
    filter_horizontal = ("janun_groups", "group_hats")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Kontakt", {"fields": ("name", "email", "address", "telephone")}),
        (
            "Berechtigungen",
            {"fields": ("is_active", "is_superuser", "role", "is_reviewed")},
        ),
        ("Gruppen", {"fields": ("janun_groups", "group_hats")}),
        ("Datum", {"fields": ("last_login", "date_joined", "updated_at")}),
    )

    def janun_groups_display(self, obj):
        return ", ".join([group.name for group in obj.janun_groups.all()])

    janun_groups_display.short_description = "Gruppen"

    def group_hats_display(self, obj):
        return ", ".join([group.name for group in obj.group_hats.all()])

    group_hats_display.short_description = "Hüte"


admin.site.register(User, UserAdmin)
