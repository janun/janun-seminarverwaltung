import unicodedata

from django import forms
from django.contrib.auth import password_validation
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from janun_seminarverwaltung.users.models import User


class UsernameField(forms.CharField):
    def to_python(self, value):
        if value:
            return unicodedata.normalize('NFKC', super().to_python(value))
        return value


class BaseUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'panel'
        self.helper.layout = Layout(
            'name', 'avatar',
            Fieldset(
                "Konto",
                'username', 'password1'
            ),
            Fieldset(
                "Kontakt-Daten",
                'email', 'phone_number', 'address'
            ),
            Fieldset(
                "Berechtigungen",
                'role', 'janun_groups', 'group_hats', 'is_reviewed'
            ),
            ButtonHolder(
                Submit('submit', 'Speichern', css_class='button button-primary'),
                css_class="panel__footer"
            )
        )

        if not self.request.user.has_perm('users.change_permissions', self.instance):
            self.fields['role'].disabled = True
            self.fields['janun_groups'].disabled = True
            self.fields['group_hats'].disabled = True
            self.fields['is_reviewed'].disabled = True

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
            messages.info(self.request, "Passwort wurde geändert.")
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = (
            'name', 'avatar', 'email', 'username', 'role',
            'janun_groups', 'group_hats', 'phone_number', 'address', 'is_reviewed'
        )
        widgets = {
            # 'role': forms.RadioSelect, # TODO: radio not working with disabled
            'phone_number': PhoneNumberInternationalFallbackWidget,
            'address': forms.Textarea(attrs={'cols': '20', 'rows': '4'}),
            # 'address': forms.TextInput()
        }
        field_classes = {'username': UsernameField}


class UserCreationForm(BaseUserForm):
    password1 = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
    )


class UserChangeForm(BaseUserForm):
    password1 = forms.CharField(
        label="Passwort Ändern",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Das alte Passwort kann nicht eingesehen werden. Aber es kann hier geändert werden."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
