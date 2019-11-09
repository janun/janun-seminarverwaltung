from django import forms
from django.urls import reverse
from django.contrib.auth import password_validation
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.account.forms import ChangePasswordForm as AllauthChangePasswordForm
from allauth.account.forms import LoginForm as AllauthLoginForm

from django_otp.plugins.otp_totp.models import TOTPDevice

from allauth_2fa.adapter import OTPAdapter
from allauth_2fa.utils import user_has_valid_totp_device

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field, Div

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField

from preferences import preferences

from backend.groups.models import JANUNGroup
from backend.utils import Link, Fieldset
from .models import User


class AccountAdapter(OTPAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit=False)
        cleaned_data = form.cleaned_data
        user.name = cleaned_data["name"]
        user.telephone = cleaned_data["telephone"]
        user.save()
        user.janun_groups.set(cleaned_data["janun_groups"])
        return user


class LoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "login",
            "password",
            Link(
                reverse("account_reset_password"),
                "Passwort vergessen?",
                "inline-block text-sm text-gray-600 hover:text-gray-800 mb-6",
            ),
            "remember",
        )

        # remove placeholders
        for field in ("login", "password"):
            del self.fields[field].widget.attrs["placeholder"]

        self.fields["login"].label = "Benutzername oder E-Mail"


class ChangePasswordForm(AllauthChangePasswordForm):
    password2 = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "password1"
        ].help_text = "Mindestens 8 Zeichen, empfohlen 12 oder mehr."
        for field in ("oldpassword", "password1"):
            del self.fields[field].widget.attrs["placeholder"]

    def clean(self):
        return super(forms.Form, self).clean()


class SignupForm(AllauthSignupForm):
    name = forms.CharField(max_length=30, label="Voller Name")
    janun_groups = forms.ModelMultipleChoiceField(
        queryset=JANUNGroup.objects.all(),
        label="JANUN-Gruppen",
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text="Wähle aus, in welchen Gruppen Du Mitglied bist.",
    )
    telephone = PhoneNumberField(
        label="Telefonnummer",
        help_text="Für dringende Rückfragen zu Deinen Seminaren",
        required=False,
        widget=PhoneNumberInternationalFallbackWidget,
        error_messages={
            "invalid": "Bitte eine gültige Telefonnummer eingeben, z.B. 0511 1241512."
        },
    )
    fax_number = forms.CharField(required=False)
    data_protection_read = forms.BooleanField(
        label="Ich habe die Datenschutzbedingungen gelesen und verstanden.",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Kontakt",
                Field("name", css_class="w-full"),
                Field("email", css_class="w-full"),
                Div(Field("telephone", css_class="w-full"), css_class="show-optional"),
                Div(
                    Field("fax_number", autocomplete="off", tabindex="-1"),
                    css_class="hidden",
                ),
                text="Wir müssen mit dir Kontakt aufnehmen können.",
            ),
            Fieldset(
                "Anmeldung",
                Field("username", css_class="w-full"),
                Field("password1", css_class="w-full"),
                text="Bitte wähle ein starkes Passwort, das du nirgends sonst verwendest. Wir empfehlen die Benutzung eines Passwortmanagers.",
            ),
            Fieldset(
                "Gruppen",
                "janun_groups",
                text="Um zu ermitteln auf welche Seminare du Zugriff hast und für wen du Seminare anmelden kannst.",
            ),
            Fieldset(
                "Datenschutz",
                "data_protection_read",
                HTML(
                    '<p class="text-gray-600">Kurz: Wir nutzen deine Daten nur für die Verwaltung der Seminare und geben sie nicht unnötig an andere weiter, aber lies selbst.</p>'
                ),
            ),
        )

        # set autofocus
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

        # set some help_texts
        self.fields["username"].help_text = "Groß-/Kleinschreibung ist egal."
        self.fields["username"].label = "Benutzername"

        self.fields[
            "email"
        ].help_text = "Du erhältst Bestätigungen, wichtige Updates und Erinnerungen zu Deinen Seminaren."

        self.fields[
            "password1"
        ].help_text = "Mindestens 8 Zeichen, empfohlen 12 oder mehr."

        # add data_protection_read url if policy setting is set
        if preferences.JANUNSeminarPreferences.data_protection_policy_url:
            self.fields[
                "data_protection_read"
            ].label = 'Ich habe die <a class="underline text-gray-900" href="{0}">Datenschutzbedingungen</a> gelesen und verstanden.'.format(
                preferences.JANUNSeminarPreferences.data_protection_policy_url
            )

        # remove placeholders
        for field in ("email", "username", "password1"):
            del self.fields[field].widget.attrs["placeholder"]

    def clean(self):
        cleaned_data = super().clean()
        # honeypot field
        fax_number = cleaned_data["fax_number"]
        if fax_number:
            self.add_error(None, "Kein Zugang für Spammer")


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        if user_has_valid_totp_device(self.request.user):
            totp_message = '<p class="text-green-600">2FA ist aktiviert.</p>'
        else:
            totp_message = '<p class="text-gray-600">2FA ist nicht aktiviert.</p>'
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Kontakt",
                Field("name", css_class="w-full"),
                Field("email", css_class="w-full"),
                Div(Field("telephone", css_class="w-full"), css_class="show-optional"),
                text="Wir müssen mit dir Kontakt aufnehmen können.",
            ),
            Fieldset(
                "Anmeldung",
                Field("username", css_class="w-full"),
                Link(
                    reverse("account_change_password"),
                    "Passwort ändern →",
                    "block font-semibold mt-8 mb-6 text-gray-700 hover:text-gray-800 hover:underline",
                ),
                Link(
                    reverse("two-factor-setup"),
                    "Zwei-Faktor-Authentisierung →",
                    "block font-semibold mb-1 text-gray-700 hover:text-gray-800 hover:underline",
                ),
                HTML(totp_message),
            ),
        )

        self.fields["username"].help_text = "Groß-/Kleinschreibung ist egal."
        self.fields["email"].required = True
        self.fields[
            "email"
        ].help_text = "Du erhältst Bestätigungen, wichtige Updates und Erinnerungen zu Deinen Seminaren."
        self.fields[
            "telephone"
        ].help_text = "Für dringende Rückfragen zu Deinen Seminaren"

        # set autofocus
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

    class Meta:
        model = User
        fields = ("name", "email", "username", "telephone")
        widgets = {"telephone": PhoneNumberInternationalFallbackWidget}


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
        required=False,
        help_text="Mindestens 8 Zeichen, empfohlen 12 oder mehr.",
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Kontakt",
                Field("name", css_class="w-full"),
                Field("email", css_class="w-full"),
                Div(Field("telephone", css_class="w-full"), css_class="show-optional"),
            ),
            Fieldset(
                "Anmeldung",
                Field("username", css_class="w-full"),
                Field("password", css_class="w-full"),
                HTML(
                    '<div class="flex justify-end">'
                    '<button type="button" data-password-field="#id_password" class="js-generate-password button text-sm font-normal bg-gray-300">Passwort generieren</button>'
                    "</div>"
                ),
            ),
            Fieldset("Berechtigungen", "is_active", "is_reviewed", "role"),
            Fieldset("Gruppen", "janun_groups", "group_hats"),
        )

        self.fields["username"].help_text = "Groß-/Kleinschreibung ist egal."
        self.fields["email"].required = True

        # set autofocus
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "username",
            "telephone",
            "is_active",
            "role",
            "is_reviewed",
            "janun_groups",
            "group_hats",
        )
        widgets = {
            "telephone": PhoneNumberInternationalFallbackWidget,
            "janun_groups": forms.CheckboxSelectMultiple,
            "group_hats": forms.CheckboxSelectMultiple,
        }


class UserDetailForm(forms.ModelForm):
    password = forms.CharField(
        label="Passwort ändern",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
        required=False,
        help_text="Leer lassen lässt es unverändert. Mindestens 8 Zeichen, empfohlen 12 oder mehr.",
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        has_totp = user_has_valid_totp_device(self.request.user)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Kontakt",
                Field("name", css_class="w-full"),
                Field("email", css_class="w-full"),
                Div(Field("telephone", css_class="w-full"), css_class="show-optional"),
            ),
            Fieldset(
                "Anmeldung",
                Field("username", css_class="w-full"),
                Field("password", css_class="w-full"),
                HTML(
                    '<div class="flex justify-end mb-4">'
                    '<button type="button" data-password-field="#id_password" class="js-generate-password button text-sm font-normal bg-gray-300">Passwort generieren</button>'
                    "</div>"
                ),
                Link(
                    reverse(
                        "users:2fa_remove", kwargs={"username": self.instance.username}
                    ),
                    "2FA ausschalten",
                    "inline-block mb-1 mt-2 font-semibold text-gray-700 hover:text-gray-800 hover:underline",
                )
                if has_totp
                else Link(
                    reverse("users:2fa", kwargs={"username": self.instance.username}),
                    "2FA einrichten",
                    "inline-block mb-1 mt-2 font-semibold text-gray-700 hover:text-gray-800 hover:underline",
                ),
                HTML('<p class="text-green-600">2FA ist aktiviert.</p>')
                if has_totp
                else HTML('<p class="text-gray-600">2FA ist nicht aktiviert.</p>'),
            ),
            Fieldset("Berechtigungen", "is_active", "is_reviewed", "role"),
            Fieldset("Gruppen", "janun_groups", "group_hats"),
        )

        if self.instance.role == "Teamer_in":
            del self.fields["group_hats"]

        self.fields["username"].help_text = "Groß-/Kleinschreibung ist egal."
        self.fields["email"].required = True

        # set autofocus
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "username",
            "telephone",
            "is_active",
            "role",
            "is_reviewed",
            "janun_groups",
            "group_hats",
        )
        widgets = {
            "telephone": PhoneNumberInternationalFallbackWidget,
            "janun_groups": forms.CheckboxSelectMultiple,
            "group_hats": forms.CheckboxSelectMultiple,
        }


class UserTOTPDeviceRemoveForm(forms.Form):
    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user

    def save(self):
        # Delete any backup tokens.
        try:
            static_device = self.user.staticdevice_set.get(name="backup")
            static_device.token_set.all().delete()
            static_device.delete()
        except ObjectDoesNotExist:
            pass

        # Delete TOTP device.
        device = TOTPDevice.objects.get(user=self.user)
        device.delete()
