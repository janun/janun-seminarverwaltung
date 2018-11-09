from django import forms

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from groups.models import JANUNGroup, ContactPerson
from widgets import ThumbnailFileInput
from janun_seminarverwaltung.users.models import User


class JANUNGroupForm(forms.ModelForm):
    group_hats = forms.ModelMultipleChoiceField(
        label="Gruppenhüte",
        queryset=User.objects.filter(role__in=("PRUEFER", "VERWALTER")),
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['group_hats'] = [g.pk for g in kwargs['instance'].group_hats.all()]
        super().__init__(*args, **kwargs)
        if not self.request.user.has_perm('groups.change_group_hats', self.instance):
            self.fields['group_hats'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.group_hats.clear()
            instance.group_hats.add(*self.cleaned_data['group_hats'])
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()
        return instance

    class Meta:
        model = JANUNGroup
        fields = ('name', 'logo', 'group_hats', 'homepage', 'email', 'address')
        widgets = {
            'logo': ThumbnailFileInput(logo=True),
            'address': forms.Textarea(attrs={'cols': '20', 'rows': '4'}),
        }


ContactPeopleInlineFormSet = forms.inlineformset_factory(
    JANUNGroup, ContactPerson, fields=('name', 'email', 'phone'),
    widgets={'phone': PhoneNumberInternationalFallbackWidget},
    max_num=3
)
