from django import forms

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from groups.models import JANUNGroup, ContactPerson


class JANUNGroupForm(forms.ModelForm):
    class Meta:
        model = JANUNGroup
        fields = ('name', 'logo', 'homepage', 'email', 'address')


ContactPeopleInlineFormSet = forms.inlineformset_factory(
    JANUNGroup, ContactPerson, fields=('name', 'email', 'phone'),
    widgets={'phone': PhoneNumberInternationalFallbackWidget},
    max_num=3
)
