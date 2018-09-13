from django import forms

from groups.models import JANUNGroup, ContactPerson


class JANUNGroupForm(forms.ModelForm):
    class Meta:
        model = JANUNGroup
        fields = ('name', 'logo', 'homepage', 'email', 'address')


ContactPeopleInlineFormSet = forms.inlineformset_factory(
    JANUNGroup, ContactPerson, fields=('name', 'email', 'phone'),
)
