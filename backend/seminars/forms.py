from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML

from .models import Seminar
from .states import all_states


class SeminarChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.editable = True
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Status",
                "status",
                HTML(
                    '<p class="text-sm mb-5 text-gray-800">{0}</p>'.format(
                        all_states["zugesagt"]["description"]
                    )
                ),
            ),
            Fieldset(
                "Inhalt",
                Field("title", css_class="w-full"),
                Field("description", css_class="w-full"),
            ),
            Fieldset(
                "Zeit & Ort",
                Div(
                    Div("start_date", css_class="mx-2"),
                    Div("start_time", css_class="mx-2"),
                    css_class="flex flex-wrap -mx-2",
                ),
                Div(
                    Div("end_date", css_class="mx-2"),
                    Div("end_time", css_class="mx-2"),
                    css_class="flex flex-wrap -mx-2",
                ),
                "location",
            ),
            Fieldset(
                "Förderung",
                "planned_training_days",
                Div(
                    Div("planned_attendees_min", css_class="mx-2"),
                    Div("planned_attendees_max", css_class="mx-2"),
                    css_class="flex flex-wrap -mx-2",
                ),
                "group",
                "requested_funding",
            ),
        )

        # disable editing for teamers if state not angemeldet:
        if not self.request or (self.instance.state != "angemeldet"):
            self.editable = False
            for key in self.Meta.fields:
                self.fields[key].disabled = True
            self.helper.layout[0].insert(
                2,
                HTML(
                    '<p class="text-sm mb-10 text-gray-800">'
                    "In diesem Status können die Seminardetails jetzt nicht (mehr) bearbeitet werden.<br>"
                    '<a class="underline href="mailto:seminare@janun.de">Kontaktiere uns</a>, '
                    "wenn noch etwas geändert werden muss.</p>"
                ),
            )

    class Meta:
        model = Seminar
        fields = (
            "status",
            "title",
            "description",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "location",
            "planned_training_days",
            "planned_attendees_min",
            "planned_attendees_max",
            "requested_funding",
            "group",
        )
