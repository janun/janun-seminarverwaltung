from django import forms

from .models import Seminar

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML
# from crispy_forms.bootstrap import Tab, TabHolder, AppendedText


class SeminarChangeForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request", None)
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_tag = False
    #     self.helper.layout = Layout(
    #         Fieldset("", "title", "content"),
    #         Fieldset(
    #             "Zeit & Ort",
    #             Div(
    #                 Div("start_date", css_class="col col-md-3"),
    #                 Div("start_time", css_class="col col-md-3"),
    #                 css_class="row",
    #             ),
    #             Div(
    #                 Div("end_date", css_class="col col-md-3"),
    #                 Div("end_time", css_class="col col-md-3"),
    #                 css_class="row",
    #             ),
    #             "location",
    #         ),
    #         Fieldset(
    #             "Förderung",
    #             "planned_training_days",
    #             Div(
    #                 Div("planned_attendees_min", css_class="col col-md-3"),
    #                 Div("planned_attendees_max", css_class="col col-md-3"),
    #                 css_class="row",
    #             ),
    #             "group",
    #             "requested_funding",
    #         ),
    #     )

    #     # disable editing for teamers if state not angemeldet:
    #     if not self.request or (
    #         self.request.user.role == "TEAMER" and self.instance.state != "ANGEMELDET"
    #     ):
    #         for key in self.Meta.fields:
    #             self.fields[key].disabled = True
    #         self.helper.layout[0][0].insert(
    #             0,
    #             HTML(
    #                 """<div class="alert alert-light">
    #                 <h5 class="alert-heading">Nicht editierbar</h5>
    #                 <p class="mb-0"><b>In diesem Status</b> können die Seminardetails jetzt nicht (mehr) bearbeitet werden.<br>
    #                 Kontaktiere uns, wenn noch etwas geändert werden muss.</p>
    #                 </div>
    #             """
    #             ),
    #         )

    class Meta:
        model = Seminar
        fields = (
            "title",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "location",
            "description",
            "planned_training_days",
            "planned_attendees_min",
            "planned_attendees_max",
            "requested_funding",
            "group",
        )
