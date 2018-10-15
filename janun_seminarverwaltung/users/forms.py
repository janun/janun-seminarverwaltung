from django import forms
from django.contrib.auth import password_validation

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from janun_seminarverwaltung.users.models import User

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        self.helper = FormHelper()
        self.helper.form_class = 'panel'
        self.helper.layout = Layout(
            Fieldset(
                "Persönliche Daten",
                'name', 'email', 'username', 'avatar', 'password'
            ),
            Fieldset(
                "Berechtigungen",
                'role', 'janun_groups', 'group_hats'
            ),
            ButtonHolder(
                Submit('submit', 'Speichern', css_class='button button-primary'),
                css_class="panel__footer"
            )
        )

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        if password:
            try:
                dummy_user = User(self.cleaned_data)
                # print("INSTANCE: ", dummy_user.__dict__)
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)

    class Meta:
        model = User
        fields = ('name', 'avatar', 'email', 'username', 'password', 'role', 'janun_groups', 'group_hats')
        widgets = {
            'role': forms.RadioSelect
        }
