from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML

from backend.groups.models import JANUNGroup
from .models import Seminar, SeminarComment
from .states import STATE_INFO, get_next_states


non_editable_text = (
    '<p class="text-sm mb-10 text-gray-800">'
    "In diesem Status können die Seminardetails jetzt nicht (mehr) bearbeitet werden.<br>"
    '<a class="underline href="mailto:seminare@janun.de">Kontaktiere uns</a>, '
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
        self.editable = True
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
            self.editable = False
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
