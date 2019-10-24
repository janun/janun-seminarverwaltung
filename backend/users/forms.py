from django import forms
from django.urls import reverse
from django.contrib.auth import password_validation

from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.account.forms import ChangePasswordForm as AllauthChangePasswordForm
from allauth_2fa.adapter import OTPAdapter

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field, Div

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField

from preferences import preferences

from backend.groups.models import JANUNGroup
from .models import User


class Link(HTML):
    def __init__(self, href, text, css_class=""):
        html = '<a class="{2}" href="{0}">{1}</a>'.format(href, text, css_class)
        super().__init__(html)


class AccountAdapter(OTPAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit=False)
        cleaned_data = form.cleaned_data
        user.name = cleaned_data["name"]
        user.telephone = cleaned_data["telephone"]
        user.save()
        user.janun_groups.set(cleaned_data["janun_groups"])
        return user


class ChangePasswordForm(AllauthChangePasswordForm):
    password2 = None

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
            "invalid": "Bitte gültige Telefonnummer eingeben, z.B. 0511 1241512"
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
                Field("telephone", css_class="w-full"),
                Div(
                    Field("fax_number", autocomplete="off", tabindex="-1"),
                    css_class="hidden",
                ),
            ),
            Fieldset(
                "Anmeldung",
                Field("username", css_class="w-full"),
                Field("password1", css_class="w-full"),
                Field("password2", css_class="w-full"),
            ),
            Fieldset("Gruppen", "janun_groups"),
            Fieldset(None, "data_protection_read"),
        )

        # set autofocus
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

        # set some help_texts
        self.fields[
            "email"
        ].help_text = "Du erhälst Bestätigungen, wichtige Updates und Erinnerungen zu Deinen Seminaren."

        self.fields[
            "username"
        ].help_text = "Erlaubt: Buchstaben, Ziffern, @-Zeichen, Punkt, Plus, Minus und Unterstrich<br>Groß-/Kleinschreibung ist egal."

        self.fields["password1"].help_text = (
            '<ul class="list-disc pl-4">'
            "<li>Mindestens 8 Zeichen, empfohlen 12 oder mehr</li>"
            "<li>Nicht nur Zahlen. (Sonderzeichen und alles andere erwünscht)</li>"
            "<li>Nicht zu ähnlich zu den anderen Feldern</li>"
            "<li>Darf kein bekanntes gehacktes Passwort sein</li>"
            "</ul>"
        )

        self.fields[
            "password1"

        # add data_protection_read url if policy setting is set
        if preferences.JANUNSeminarPreferences.data_protection_policy_url:
            self.fields[
                "data_protection_read"
            ].label = 'Ich habe die <a class="underline" href="{0}">Datenschutzbedingungen</a> gelesen und verstanden.'.format(
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
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Kontakt",
                Field("name", css_class="w-full"),
                Field("email", css_class="w-full"),
                Field("telephone", css_class="w-full"),
            ),
            Fieldset(
                "Anmeldung",
                "username",
                Link(
                    reverse("account_change_password"),
                    "Passwort ändern →",
                    "block mb-6 mt-4 text-gray-700 hover:text-gray-800",
                ),
                Link(
                    reverse("two-factor-setup"),
                    "Zwei-Faktor-Authentisierung →",
                    "block text-gray-700 hover:text-gray-800",
                ),
            ),
        )

        self.fields["username"].help_text = ""
        self.fields["email"].required = True
        self.fields[
            "email"
        ].help_text = "Du erhälst Bestätigungen, wichtige Updates und Erinnerungen zu Deinen Seminaren."
        self.fields[
            "telephone"
        ].help_text = "Für dringende Rückfragen zu Deinen Seminaren"

        # set autofocus
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

    class Meta:
        model = User
        fields = ("name", "email", "username", "telephone")
        widgets = {"telephone": PhoneNumberInternationalFallbackWidget}
