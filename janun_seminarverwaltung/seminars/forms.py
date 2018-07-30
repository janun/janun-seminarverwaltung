from django import forms

from seminars.models import Seminar


class SeminarStepForm(forms.ModelForm):
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ContentSeminarForm(SeminarStepForm):
    class Meta:
        model = Seminar
        title = "Um was geht es bei Deinem Seminar?"
        short_title = "Inhalt"
        fields = ('title', 'content')


class DatetimeSeminarForm(SeminarStepForm):
    class Meta:
        model = Seminar
        title = "Wann findet Dein Seminar statt?"
        short_title = "Datum"
        fields = ('start', 'end')


class LocationSeminarForm(SeminarStepForm):
    class Meta:
        model = Seminar
        title = "Wo findet Dein Seminar statt?"
        short_title = "Ort"
        fields = ('location',)


class TrainingDaysSeminarForm(SeminarStepForm):
    class Meta:
        model = Seminar
        title = "Wieviele Bildungstage hat Dein Seminar?"
        short_title = "Bildungstage"
        fields = ('planned_training_days',)


class AttendeesSeminarForm(SeminarStepForm):
    class Meta:
        model = Seminar
        title = "Mit wievielen Teilnehmenden rechnest Du?"
        short_title = "Teilnehmende"
        fields = ('planned_attendees',)


class GroupSeminarForm(SeminarStepForm):
    class Meta:
        model = Seminar
        title = "Meldest Du das Seminar für eine JANUN-Gruppe an?"
        short_title = "Gruppe"
        fields = ('group',)


class FundingSeminarForm(SeminarStepForm):
    class Meta:
        model = Seminar
        title = "Wieviel Förderung benötigst Du?"
        short_title = "Förderung"
        fields = ('requested_funding',)
