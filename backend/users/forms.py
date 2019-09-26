from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field

from backend.groups.models import JANUNGroup
from .models import User


class Link(HTML):
    def __init__(self, href, text, css_class=""):
        html = '<a class="{2}" href="{0}">{1}</a>'.format(href, text, css_class)
        super().__init__(html)


data_protection_url = (
    "https://www.janun.de/documents/111/Datenverarbeitung_Seminarabrechnung.pdf"
)


class SignupForm(forms.Form):
    name = forms.CharField(max_length=30, label="Voller Name")
    janun_groups = forms.ModelMultipleChoiceField(
        queryset=JANUNGroup.objects.all(), label="JANUN-Gruppe(n)", required=False
    )
    data_protection_read = forms.BooleanField(
        label='Ich habe die <a class="underline" href="{0}">Datenschutzbedingungen</a> gelesen und verstanden.'.format(
            data_protection_url
        ),
        required=True,
    )
    telephone = forms.CharField(max_length=100, label="Telefonnummer", required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Kontakt", "name", "email", "telephone"),
            Fieldset("Anmeldung", "username", "password1", "password2"),
            Fieldset("Gruppen", "janun_groups"),
            Fieldset(None, "data_protection_read"),
        )

        # set autofocus
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

    def signup(self, request, user):
        user.name = self.cleaned_data["name"]
        user.janun_groups.set(self.cleaned_data["janun_groups"])
        user.telephone = self.cleaned_data["telephone"]
        user.save()


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
                Field("address", css_class="w-full resize-none"),
            ),
            Fieldset(
                "Anmeldung",
                "username",
                Link(
                    reverse("account_change_password"),
                    "Passwort ändern →",
                    "block mb-6 mt-4 text-gray-700 hover:text-gray-900",
                ),
                Link(
                    reverse("two-factor-setup"),
                    "Zwei-Faktor-Authentisierung →",
                    "block text-gray-700 hover:text-gray-900",
                ),
            ),
        )

        self.fields["username"].help_text = ""
        self.fields["address"].widget.attrs.update({"rows": 3})

    class Meta:
        model = User
        fields = ("name", "email", "username", "telephone", "address")
