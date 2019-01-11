from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from crispy_forms.bootstrap import Tab, TabHolder


from seminars.models import Seminar, SeminarComment


def validate_delete(value):
    if value != "löschen":
        raise ValidationError("Du musst „löschen“ eingeben")


class DeleteForm(forms.Form):
    delete = forms.CharField(
        label="Gib „löschen“ ein", required=True, validators=[validate_delete],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'].widget.attrs['pattern'] = "löschen"


class SeminarChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab('Inhalt',
                    'title',
                    'content',
                   ),
                Tab('Zeit & Ort',
                    Div(
                        Div('start_date', css_class='col col-md-3'),
                        Div('start_time', css_class='col col-md-3'),
                        css_class='row'
                    ),
                    Div(
                        Div('end_date', css_class='col col-md-3'),
                        Div('end_time', css_class='col col-md-3'),
                        css_class='row'
                    ),
                    'location',
                   ),
                Tab('Förderung',
                    'planned_training_days',
                    Div(
                        Div('planned_attendees_min', css_class='col col-md-3'),
                        Div('planned_attendees_max', css_class='col col-md-3'),
                        css_class='row'
                    ),
                    'group',
                    'requested_funding',
                   ),
               Tab('Abrechnung',

                  )
            )
        )
        # disable editing for teamers:
        if not self.request or (self.request.user.role == 'TEAMER' and self.instance.state != 'ANGEMELDET'):
            for key in self.Meta.fields:
                self.fields[key].disabled = True

    class Meta:
        model = Seminar
        fields = ('title', 'start_date', 'start_time', 'end_date', 'end_time', 'location', 'content',
                  'planned_training_days', 'planned_attendees_min', 'planned_attendees_max',
                  'requested_funding', 'group')


class SeminarCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "Dein Kommentar"}),
        label='',
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if not self.request or not self.request.user.has_perm('seminars.create_internal_comment', self.instance):
            self.fields['is_internal'].widget = forms.HiddenInput()

    class Meta:
        model = SeminarComment
        fields = ('comment', 'is_internal')


class SeminarStepForm(forms.ModelForm):
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        list(self.fields.values())[0].widget.attrs['autofocus'] = 'autofocus'

    class Meta:
        model = Seminar
        fields = ()


class ContentSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Um was geht es bei Deinem Seminar?"
        short_title = "Inhalt"
        fields = ('title', 'content')


class DatetimeSeminarForm(SeminarStepForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Div('start_date', css_class='col'),
                Div('start_time', css_class='col'),
                css_class='row'
            ),
            Div(
                Div('end_date', css_class='col'),
                Div('end_time', css_class='col'),
                css_class='row'
            ),
        )

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if self.user.role == 'TEAMER' and start_date < (timezone.now().date() + timedelta(days=14)):
            raise forms.ValidationError("Sorry, Du musst Dein Seminar 14 Tage vorher anmelden.")
        return start_date

    class Meta(SeminarStepForm.Meta):
        title = "Wann findet Dein Seminar statt?"
        short_title = "Datum"
        fields = ('start_date', 'start_time', 'end_date', 'end_time')


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Div(
                Div('planned_attendees_min', css_class='col'),
                Div('planned_attendees_max', css_class='col'),
                css_class='row'
            ),
        )

    class Meta(SeminarStepForm.Meta):
        title = "Mit wievielen Teilnehmenden rechnest Du?"
        short_title = "Teilnehmende"
        fields = ('planned_attendees_min', 'planned_attendees_max')


class GroupSeminarForm(SeminarStepForm):
    has_group = forms.TypedChoiceField(
        label="",
        coerce=lambda x: x == 'True',
        choices=(
            (False, "Nein, Anmeldung als Einzelperson"),
            (True, "Ja, für folgende Gruppe:"),
        ),
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')
        if user.janun_groups.count() == 1:
            kwargs['initial']['group'] = user.janun_groups.get()
        kwargs['initial']['has_group'] = user.janun_groups.exists()
        super().__init__(*args, **kwargs)
        # if user.role == 'TEAMER':
        #     self.fields['group'].queryset = user.janun_groups
        self.fields['group'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        has_group = cleaned_data.get('has_group')
        group = cleaned_data.get('group')
        if has_group and not group:
            self.add_error('group', "Du musst eine Gruppe auswählen.")
        # if has_group and self.user.role == 'TEAMER' and not self.user.janun_groups.exists():
        #     self.add_error('has_group', "Du musst Mitglied in einer Gruppe sein.")
        if not has_group:
            cleaned_data['group'] = None

    class Meta(SeminarStepForm.Meta):
        title = "Meldest Du das Seminar für eine JANUN-Gruppe an?"
        short_title = "Gruppe"
        fields = ('has_group', 'group')


class FundingSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Wieviel Förderung benötigst Du?"
        short_title = "Förderung"
        fields = ('requested_funding',)


class BarrierSeminarForm(SeminarStepForm):
    class Meta(SeminarStepForm.Meta):
        title = "Auftretende Barrieren"
        short_title = "Barrieren"
        fields = ('mobility_barriers', 'language_barriers', 'hearing_barriers', 'seeing_barriers')
        widgets = {
            'mobility_barriers': forms.Textarea(attrs={'rows': '3'}),
            'language_barriers': forms.Textarea(attrs={'rows': '3'}),
            'hearing_barriers': forms.Textarea(attrs={'rows': '3'}),
            'seeing_barriers': forms.Textarea(attrs={'rows': '3'}),
        }


class ConfirmSeminarForm(SeminarStepForm):
    confirm_policy = forms.BooleanField(
        label="""Ich habe die
                 <a target=\"_blank\" href=\"{}\">Seminarabrechnungsrichtlinie</a>
                 gelesen.""".format(settings.SEMINAR_POLICY_URL),
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
                label="Ich möchte die <b>Förderung von {} €</b> beantragen.".format(self.instance.requested_funding),
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
