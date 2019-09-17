from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML

from backend.groups.models import JANUNGroup
from .models import User


class Link(HTML):
    def __init__(self, href, text, css_class=""):
        html = '<a class="{2}" href="{0}">{1}</a>'.format(href, text, css_class)
        super().__init__(html)


class SignupForm(forms.Form):
    name = forms.CharField(max_length=30, label="Voller Name")
    janun_groups = forms.ModelMultipleChoiceField(
        queryset=JANUNGroup.objects.all(), label="JANUN-Gruppe(n)", required=False
    )
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
            Fieldset("Kontakt", "name", "email", "telephone"),
            Fieldset("Anmeldung", "username", "password1", "password2"),
            Fieldset("Gruppen", "janun_groups"),
            Fieldset(None, "data_protection_read"),
        )

    def signup(self, request, user):
        user.name = self.cleaned_data["name"]
        user.janun_groups.set(self.cleaned_data["janun_groups"])
        user.save()


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Kontakt", "name", "email", "telephone"),
            Fieldset(
                "Anmeldung",
                "username",
                Link(
                    reverse("account_change_password"),
                    "Passwort ändern",
                    "text-gray-700 underline",
                ),
            ),
        )

    class Meta:
        model = User
        fields = ("name", "email", "username", "telephone")
