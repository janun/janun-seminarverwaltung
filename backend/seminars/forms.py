from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML

from backend.groups.models import JANUNGroup
from .models import Seminar, SeminarComment
from .states import STATE_INFO, get_next_states


non_editable_text = (
    '<p class="text-sm mb-10 text-gray-800">'
    "In diesem Status können die Seminardetails jetzt nicht (mehr) bearbeitet werden."
    '<br><a class="underline" href="mailto:seminare@janun.de">Kontaktiere uns</a>, '
    "wenn noch etwas geändert werden muss.</p>"
)


class SeminarChangeForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Dein Kommentar", "class": "w-full"}
        ),
        required=False,
        label="Kommentar",
    )

    def get_state_description(self):
        html = '<p class="text-sm font-bold mb-5 text-gray-800">{0}</p>'.format(
            STATE_INFO[self.instance.status]["description"]
        )
        if self.instance.status == "überwiesen" and self.instance.transferred_at:
            html = '<p class="text-sm font-bold mb-5 text-gray-800">Am {0} überwiesen.</p>'.format(
                self.instance.transferred_at.strftime("%d.%m.%Y")
            )
        return html

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Status", "status", HTML(self.get_state_description())),
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
                    css_class="md:flex -mx-2",
                ),
                Div(
                    Div("end_date", css_class="mx-2"),
                    Div("end_time", css_class="mx-2"),
                    css_class="md:flex -mx-2",
                ),
                "location",
            ),
            Fieldset(
                "Förderung",
                "planned_training_days",
                Div(
                    Div("planned_attendees_min", css_class="mx-2"),
                    Div("planned_attendees_max", css_class="mx-2"),
                    css_class="md:flex -mx-2",
                ),
                "group",
                "requested_funding",
            ),
            "comment",
        )

        # set possible status choices:
        possible_states = get_next_states(self.instance.status) + [self.instance.status]
        self.fields["status"].choices = [(status, status) for status in possible_states]

        # set possible group choices:
        group_pks = [group.pk for group in self.request.user.janun_groups.all()]
        if self.instance.group:
            group_pks += [self.instance.group.pk]
        possible_groups = JANUNGroup.objects.filter(pk__in=group_pks)
        self.fields["group"].queryset = possible_groups

        # disable editing if state not angemeldet:
        if self.instance.status != "angemeldet":
            for key in self.Meta.seminar_fields:
                if key != "status":
                    self.fields[key].disabled = True
            self.helper.layout[1].insert(0, HTML(non_editable_text))
            self.helper.layout[2].insert(0, HTML(non_editable_text))
            self.helper.layout[3].insert(0, HTML(non_editable_text))

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if self.cleaned_data["comment"]:
            comment = SeminarComment(
                text=self.cleaned_data["comment"],
                seminar=instance,
                owner=self.request.user,
            )
            comment.save()
            self.instance.comments.add(comment)
        return instance

    class Meta:
        model = Seminar
        seminar_fields = (
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
        fields = seminar_fields + ("comment",)


class SeminarStepForm(forms.ModelForm):
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        list(self.fields.values())[0].widget.attrs["autofocus"] = "autofocus"

    class Meta:
        model = Seminar
        title = ""
        short_title = ""
        fields = ()


class ContentSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            HTML(
                '<p class="mb-4 text-gray-700">Beschreibe uns Dein Seminar, '
                "damit wir entscheiden können, ob wir es fördern können.</p>"
            ),
            "title",
            "description",
        )
        self.fields["title"].required = True
        self.fields["description"].required = True

    class Meta(SeminarStepForm.Meta):
        title = "Seminarinhalte"
        short_title = "Inhalt"
        fields = ("title", "description")


class DateLocationSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Div("start_date", css_class="mx-2"),
                Div("start_time", css_class="mx-2"),
                css_class="flex -mx-2",
            ),
            Div(
                Div("end_date", css_class="mx-2"),
                Div("end_time", css_class="mx-2"),
                css_class="flex -mx-2",
            ),
            "location",
        )
        self.fields["start_date"].required = True
        self.fields["end_date"].required = True

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date and start_date:
            if end_date < start_date:
                msg = "Muss nach Start-Datum liegen"
                self.add_error("end_date", msg)

    class Meta(SeminarStepForm.Meta):
        model = Seminar
        title = "Wann & Wo"
        short_title = "Wann & Wo"
        fields = ("start_date", "start_time", "end_date", "end_time", "location")


class TrainingDaysSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["planned_training_days"].required = True

    class Meta(SeminarStepForm.Meta):
        title = "Wieviele Bildungstage hat Dein Seminar?"
        short_title = "Bildungstage"
        fields = ("planned_training_days",)


class AttendeesSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Div("planned_attendees_min", css_class="mx-2"),
                Div("planned_attendees_max", css_class="mx-2"),
                css_class="flex -mx-2",
            )
        )
        self.fields["planned_attendees_min"].required = True
        self.fields["planned_attendees_max"].required = True

    def clean(self):
        cleaned_data = super().clean()
        planned_attendees_min = cleaned_data.get("planned_attendees_min")
        planned_attendees_max = cleaned_data.get("planned_attendees_max")
        if planned_attendees_max and planned_attendees_min:
            if planned_attendees_max < planned_attendees_min:
                msg = "Muss größer/gleich dem Minimalwert sein."
                self.add_error("planned_attendees_max", msg)

    class Meta(SeminarStepForm.Meta):
        title = "Mit wievielen Teilnehmenden rechnest Du?"
        short_title = "Teilnehmende"
        fields = ("planned_attendees_min", "planned_attendees_max")


class GroupSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        user = kwargs["request"].user
        if user.janun_groups.count() == 1:
            kwargs["initial"]["group"] = user.janun_groups.get()
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = user.janun_groups

    class Meta(SeminarStepForm.Meta):
        title = "Meldest Du das Seminar für eine JANUN-Gruppe an?"
        short_title = "Gruppe"
        fields = ("group",)


class FundingSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Wieviel Förderung benötigst Du?"
        short_title = "Förderung"
        fields = ("requested_funding",)


class ConfirmSeminarForm(SeminarStepForm):
    confirm_policy = forms.BooleanField(
        label='Ich habe die <a class="underline" target="_blank" href="{}">'
        "Seminarabrechnungsrichtlinie</a> gelesen.".format(
            "https://www.janun.de/downloads"
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.requested_funding:
            self.fields["confirm_funding"] = forms.BooleanField(
                label="Ich möchte die <b>Förderung von {} €</b> beantragen.".format(
                    self.instance.requested_funding
                ),
                required=True,
            )

        deadline = self.instance.get_deadline()
        if deadline:
            self.fields["confirm_deadline"] = forms.BooleanField(
                label="Ich reiche alle Unterlagen bis zur <b>Abrechnungsdeadline am {}</b> ein.".format(
                    deadline.strftime("%d.%m.%Y")
                ),
                required=True,
            )

    class Meta(SeminarStepForm.Meta):
        title = "Bestätigung"
        short_title = "Bestätigung"
