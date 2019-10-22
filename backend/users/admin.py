from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.account.models import EmailAddress
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from import_export import fields, resources
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportMixin
from preferences.admin import PreferencesAdmin

from backend.groups.models import JANUNGroup
from .models import User, JANUNSeminarPreferences

# remove unused apps from admin
admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)

# enforce normal login for admin login
admin.site.login = login_required(admin.site.login)

admin.site.site_header = "JANUN Seminarverwaltung"
admin.site.site_title = "JANUN Seminarverwaltung"
admin.site.index_title = "JANUN Seminarverwaltung"
admin.site.site_url = None


admin.site.register(JANUNSeminarPreferences, PreferencesAdmin)


class UserResource(resources.ModelResource):
    janun_groups = fields.Field(
        column_name="janun_groups",
        attribute="janun_groups",
        widget=ManyToManyWidget(JANUNGroup, field="name"),
    )

    group_hats = fields.Field(
        column_name="group_hats",
        attribute="group_hats",
        widget=ManyToManyWidget(JANUNGroup, field="name"),
    )

    class Meta:
        model = User


class UserAdmin(ImportExportMixin, BaseUserAdmin):
    resource_class = UserResource
    search_fields = ["name", "username"]
    save_on_top = True
    list_display = (
        "name",
        "role",
        "janun_groups_display",
        "group_hats_display",
        "is_reviewed",
        "is_active",
        "last_visit",
    )
    list_filter = (
        "role",
        "is_reviewed",
        ("janun_groups", RelatedDropdownFilter),
        ("group_hats", RelatedDropdownFilter),
    )
    readonly_fields = ("date_joined", "updated_at", "last_visit")
    filter_horizontal = ("janun_groups", "group_hats")
    radio_fields = {"role": admin.VERTICAL}

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Kontakt", {"fields": ("name", "email", "telephone")}),
        ("Berechtigungen", {"fields": ("is_active", "is_reviewed", "role")}),
        ("Gruppen", {"fields": ("janun_groups", "group_hats")}),
        ("Datum", {"fields": ("last_visit", "date_joined", "updated_at")}),
    )

    def janun_groups_display(self, obj):
        return ", ".join([group.name for group in obj.janun_groups.all()])

    janun_groups_display.short_description = "Gruppen"

    def group_hats_display(self, obj):
        return ", ".join([group.name for group in obj.group_hats.all()])

    group_hats_display.short_description = "Hüte"


admin.site.register(User, UserAdmin)
