from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update(
        {"duplicate_username": "This username has already been taken."}
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages["duplicate_username"])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ['username', 'name', 'role', 'get_groups']
    search_fields = ['name']
    add_fieldsets = (
        ('', {'fields': ('username', 'password1', 'password2', 'role', 'name')}),
    )

    # fieldsets = (("User Profile", {"fields": ("name",)}),) + AuthUserAdmin.fieldsets

    def get_groups(self, obj):
        groups = []
        if obj.role == "TEAMER":
            groups = obj.janun_groups.all()
        else:
            groups = obj.group_hats.all()
        return "\n".join([g.name for g in groups])
    get_groups.short_description = 'Gruppen'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return (
                ('', {'fields': ('username', 'password1', 'password2', 'role', 'name')}),
            )
        fieldsets = [
            ('', {'fields': ('username', 'password')}),
            ('Persönliche Infos', {'fields': ('name', 'email', 'avatar')}),
            ('Berechtigungen', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
        ]
        if obj.role == User.ROLES.TEAMER:
            fieldsets.append(('Gruppen', {'fields': ('janun_groups',)}),)
        if obj.role == User.ROLES.PRUEFER:
            fieldsets.append(('Gruppen', {'fields': ('group_hats',)}),)
        fieldsets.append(('Verschiedenes', {'fields': ('last_login', 'date_joined')}),)
        return fieldsets
