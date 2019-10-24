from django import forms
from django.utils import timezone, formats
from django.core.validators import MinValueValidator, MaxValueValidator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML
from crispy_forms.bootstrap import AppendedText
from preferences import preferences

from backend.groups.models import JANUNGroup
from .models import Seminar
from .states import STATE_INFO, get_next_states


class SeminarChangeForm(forms.ModelForm):
    def get_state_description(self):
        text = STATE_INFO[self.instance.status]["description"]
        if self.instance.status == "überwiesen" and self.instance.transferred_at:
            text = "Am {0} überwiesen.".format(
                self.instance.transferred_at.strftime("%d.%m.%Y")
            )
        html = '<p class="text-sm mb-2 -mt-2 text-gray-700">{0}</p>'.format(text)
        if self.instance.status != "angemeldet":
            html += '<p class="text-sm mb-5">Seminardetails können jetzt nicht mehr geändert werden.</p>'
        return html

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.disabled = False
        self.show_save_button = True
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("Status", "status", HTML(self.get_state_description())),
            Fieldset(
                "Inhalt",
                Field("title", css_class="w-full"),
                Field("description", css_class="w-full js-autogrow"),
            ),
            Fieldset(
                "Zeit & Ort",
                Div(
                    Div(Field("start_date", css_class="w-32"), css_class="mx-2"),
                    Div(Field("start_time", css_class="w-24"), css_class="mx-2"),
                    css_class="flex -mx-2",
                ),
                Div(
                    Div(Field("end_date", css_class="w-32"), css_class="mx-2"),
                    Div(Field("end_time", css_class="w-24"), css_class="mx-2"),
                    css_class="flex -mx-2",
                ),
                Field("location", css_class="w-full"),
            ),
            Fieldset(
                "Förderung",
                Field("planned_training_days", css_class="w-24"),
                Div(
                    Div(
                        Field("planned_attendees_min", css_class="w-24"),
                        css_class="mx-2",
                    ),
                    Div(
                        Field("planned_attendees_max", css_class="w-24"),
                        css_class="mx-2",
                    ),
                    css_class="md:flex -mx-2",
                ),
                "group",
                AppendedText("requested_funding", "€", css_class="w-40"),
            ),
            "comment",
        )

        self.fields["start_date"].help_text = "z.B. {}".format(
            timezone.now().today().strftime("%d.%m.%Y")
        )
        self.fields["start_time"].help_text = "z.B. 15:00"

        # validate funding:
        max_funding = self.instance.get_max_funding()
        if max_funding:
            self.fields["requested_funding"].validators = [
                MaxValueValidator(max_funding)
            ]

        # set possible status choices:
        next_states = get_next_states(self.instance.status)
        possible_states = [self.instance.status] + next_states
        self.fields["status"].choices = [(status, status) for status in possible_states]

        # set possible group choices:
        group_pks = [group.pk for group in self.request.user.janun_groups.all()]
        if self.instance.group:
            group_pks += [self.instance.group.pk]
        possible_groups = JANUNGroup.objects.filter(pk__in=group_pks)
        self.fields["group"].queryset = possible_groups

        # disable editing if state not angemeldet:
        if self.instance.status != "angemeldet":
            self.disabled = True
            for key in self.Meta.fields:
                if key != "status":
                    self.fields[key].disabled = True
                    self.fields[key].widget.attrs.update(
                        title="Kann in diesem Status nicht geändert werden."
                    )

        if self.disabled and not next_states:
            self.show_save_button = False

        if not self.request.user == self.instance.owner:
            self.show_save_button = False

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
        widgets = {"status": forms.RadioSelect}


class SeminarStepForm(forms.ModelForm):
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # set autofocus on the first field
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
                '<p class="mb-4 text-gray-800">Beschreibe uns Dein Seminar, '
                "damit wir entscheiden können, ob wir es fördern können.</p>"
            ),
            Field("title", css_class="w-full"),
            Field("description", css_class="w-full js-autogrow"),
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
                Div(Field("start_date", css_class="w-32"), css_class="mx-2"),
                Div(Field("start_time", css_class="w-24"), css_class="mx-2"),
                css_class="flex -mx-2",
            ),
            Div(
                Div(Field("end_date", css_class="w-32"), css_class="mx-2"),
                Div(Field("end_time", css_class="w-24"), css_class="mx-2"),
                css_class="flex -mx-2",
            ),
            Field("location", css_class="w-full"),
        )
        self.fields["start_date"].required = True
        self.fields["start_date"].help_text = "z.B. {}".format(
            timezone.now().today().strftime("%d.%m.%Y")
        )
        self.fields["start_time"].help_text = "z.B. 15:00"
        self.fields["end_date"].required = True

    class Meta(SeminarStepForm.Meta):
        model = Seminar
        title = "Wann & Wo"
        short_title = "Wann & Wo"
        fields = ("start_date", "start_time", "end_date", "end_time", "location")


class TrainingDaysSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field("planned_training_days", css_class="w-32"),
            HTML(
                "<p>Bildungstage sind Tage, an denen <strong>min. 6 Zeitstunden Bildungsarbeit</strong> stattfinden.</p>"
                '<h4 class="mt-4 mb-1 font-bold">2-tägige Seminare am Wochenende (Fr/Sa & Sa/So)</h4>'
                "<p>sind schon 2 Bildungstage, wenn insg. 8 Stunden Bildungsarbeit stattfinden.</p>"
                '<h4 class="mt-4 mb-1 font-bold">An- und Abreisetage</h4>'
                "<p>sind zusammen 1 Bildungstag, wenn an beiden zusammen min. 6 Zeitstunden Bildungsarbeit stattfinden.</p>"
                "<p>sind je 1 Bildungstag, wenn außerdem am Anreisetag vor 12 Uhr begonnen wird und am Abreisetag nach 15.30 Uhr geendet wird.</p>"
            ),
        )
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
                Div(Field("planned_attendees_min", css_class="w-24"), css_class="mx-2"),
                Div(Field("planned_attendees_max", css_class="w-24"), css_class="mx-2"),
                css_class="flex -mx-2",
            ),
            HTML(
                '<p class="mt-4">Seminare mit <strong>weniger als 10</strong> Teilnehmenden können nicht gefördert werden. '
                "Die Förderung geht nur <strong>bis 40</strong> Teilnehmende, aber Ausnahmen sind manchmal möglich.</p>"
                '<h4 class="mt-6 mb-1 font-bold">Mehr als die Hälfte der Teilnehmenden:</h4>'
                '<ul class="list-disc ml-4">'
                "<li>müssen ihren Wohnsitz in Niedersachsen haben.</li>"
                "<li>müssen mindestens 12 Jahre alt sein und maximal 27.</li>"
                "</ul>"
                "<p>Diese Quoten müssen über den gesamten Seminarzeitraum eingehalten werden.</p>"
            ),
        )
        self.fields["planned_attendees_min"].required = True
        self.fields["planned_attendees_min"].validators = [MinValueValidator(10)]
        self.fields["planned_attendees_min"].label = "Mindestens"
        self.fields["planned_attendees_max"].required = True
        self.fields["planned_attendees_max"].label = "Maximal"

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        max_funding = self.instance.get_max_funding()
        if max_funding:
            funding_text = (
                "<p>Du kannst <strong>maximal {} €</strong> beantragen.</p>"
                '<p class="mb-4">Solltest Du aber auch mit weniger Förderung auskommen, '
                "können evtl. mehr Seminare bei JANUN stattfinden.</p>"
            ).format(formats.localize(max_funding, use_l10n=True))
            self.fields["requested_funding"].validators = [
                MaxValueValidator(max_funding)
            ]
        else:
            funding_text = ""

        self.helper.layout = Layout(
            HTML(funding_text),
            AppendedText("requested_funding", "€"),
            HTML(
                '<p class="text-sm mt-4">JANUN fördert Seminare, finanziert sie aber nicht komplett. '
                "Deswegen brauchst Du auch andere Einnahmen (Teilnahmebeiträge, Spenden o.ä.). "
                "Der Richtwert für Teilnahmebeiträge ist 3,50 € pro Person und Tag. "
                "Ausgenommen sind eintägige Seminare.</p>"
            ),
        )
        self.fields["requested_funding"].required = True

    class Meta(SeminarStepForm.Meta):
        title = "Wieviel Förderung benötigst Du?"
        short_title = "Förderung"
        fields = ("requested_funding",)


class ConfirmSeminarForm(SeminarStepForm):
    confirm_policy = forms.BooleanField(
        label="Ich habe die Seminarabrechnungsrichtlinie gelesen.", required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if preferences.JANUNSeminarPreferences.seminar_policy_url:
            self.fields["confirm_policy"].label = (
                'Ich habe die <a class="underline" target="_blank" href="{}">'
                "Seminarabrechnungsrichtlinie</a> gelesen."
            ).format(preferences.JANUNSeminarPreferences.seminar_policy_url)

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
