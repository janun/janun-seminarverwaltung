from django import forms
from django.core import validators
from django.conf import settings

from seminars.models import Seminar


class UserMixin:
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)


class SeminarStepForm(UserMixin, forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Seminar
        fields = ()


class ContentSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Um was geht es bei Deinem Seminar?"
        short_title = "Inhalt"
        fields = ('title', 'content')


class DatetimeSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Wann findet Dein Seminar statt?"
        short_title = "Datum"
        fields = ('start', 'end')


class LocationSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Wo findet Dein Seminar statt?"
        short_title = "Ort"
        fields = ('location',)


class TrainingDaysSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Wieviele Bildungstage hat Dein Seminar?"
        short_title = "Bildungstage"
        fields = ('planned_training_days',)


class AttendeesSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Mit wievielen Teilnehmenden rechnest Du?"
        short_title = "Teilnehmende"
        fields = ('planned_attendees',)


class GroupSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')
        if user.role == 'TEAMER' and user.janun_groups.count() == 1:
            kwargs['initial']['group'] = user.janun_groups.get()
        super().__init__(*args, **kwargs)
        if user.role == 'TEAMER':
            self.fields['group'].queryset = user.janun_groups

    class Meta(SeminarStepForm.Meta):
        title = "Meldest Du das Seminar für eine JANUN-Gruppe an?"
        short_title = "Gruppe"
        fields = ('group',)


class FundingSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Wieviel Förderung benötigst Du?"
        short_title = "Förderung"
        fields = ('requested_funding',)


class ConfirmSeminarForm(SeminarStepForm):
    confirm_policy = forms.BooleanField(
        label="Ich habe die <a href='%s'>Seminarabrechnungsrichtlinie</a> gelesen." % settings.SEMINAR_POLICY_URL,
        required=True,
    )

    confirm_deadline = forms.BooleanField(
        label="Ich reiche alle Unterlagen bis zur Abrechnungsdeadline ein.",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.requested_funding:
            self.fields['confirm_funding'] = forms.BooleanField(
                label="Ich möchte die <b>Förderung von %s €</b> beantragen." % self.instance.requested_funding,
                required=True,
            )

        deadline = self.instance.get_deadline()
        if deadline:
            label = "Ich reiche alle Unterlagen bis zur <b>Abrechnungsdeadline am %s</b> ein." % \
                deadline.strftime("%d.%m.%Y")
            self.fields['confirm_deadline'].label = label

    class Meta(SeminarStepForm.Meta):
        title = "Bestätigung"
        short_title = "Bestätigung"
