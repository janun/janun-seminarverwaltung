from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import AppendedText
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from backend.utils import Fieldset
from backend.seminars.models import FundingRate

from backend.users.models import JANUNSeminarPreferences


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Kontakt-Daten",
                Field("help_phone", css_class="w-full"),
                Field("help_email", css_class="w-full"),
            ),
            Fieldset(
                "Links",
                Field("seminar_policy_url", css_class="w-full"),
                Field("data_protection_policy_url", css_class="w-full"),
                Field("legal_url", css_class="w-full"),
            ),
        )

    class Meta:
        model = JANUNSeminarPreferences
        fields = (
            "help_phone",
            "help_email",
            "seminar_policy_url",
            "data_protection_policy_url",
            "legal_url",
        )
        widgets = {"help_phone": PhoneNumberInternationalFallbackWidget}


class FundingRateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", Field("year")),
            Fieldset(
                "JANUN-Gruppen",
                AppendedText("group_rate", "€"),
                AppendedText("group_rate_one_day", "€"),
                Field("group_limit_formula", css_class="w-full"),
                AppendedText("group_limit", "€"),
                text="Förderung für Seminare, die für JANUN-Gruppen angemeldet werden.",
            ),
            Fieldset(
                "Einzelpersonen",
                AppendedText("single_rate", "€"),
                AppendedText("single_rate_one_day", "€"),
                Field("single_limit_formula", css_class="w-full"),
                AppendedText("single_limit", "€"),
                text="Förderung für Seminare, die für Einzelpersonen angemeldet werden.",
            ),
        )

        for field in (
            "group_rate",
            "group_rate_one_day",
            "group_limit",
            "single_rate",
            "single_rate_one_day",
            "single_limit",
        ):
            self.fields[field].widget.attrs["min"] = 0

        if self.instance.pk:
            self.fields["year"].disabled = True

    class Meta:
        model = FundingRate
        group_fields = (
            "group_rate",
            "group_rate_one_day",
            "group_limit_formula",
            "group_limit",
        )
        single_fields = (
            "single_rate",
            "single_rate_one_day",
            "single_limit_formula",
            "single_limit",
        )
        fields = ("year",) + group_fields + single_fields
        widgets = {
            "group_limit_formula": forms.Textarea(attrs={"rows": 2}),
            "single_limit_formula": forms.Textarea(attrs={"rows": 2}),
        }
