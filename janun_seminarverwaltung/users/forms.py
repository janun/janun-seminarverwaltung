import unicodedata

from django import forms
from django.contrib.auth import password_validation
from django.contrib import messages
from django.urls import reverse_lazy

from allauth.account.forms import LoginForm, SignupForm, SetPasswordField
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field

from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField


from janun_seminarverwaltung.users.models import User
from groups.models import JANUNGroup
from widgets import ThumbnailFileInput


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
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'email',
            'username',
            'password1',
            'avatar',
            Fieldset(
                "Kontakt-Daten",
                'phone_number', 'address',
                id="contact"
            ),
            Fieldset(
                "Berechtigungen",
                'role', 'janun_groups', 'group_hats', 'is_reviewed',
                id="permissions"
            ),
        )
        if not self.errors:
            self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

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
            if user.pk and self.request:
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
            'phone_number': PhoneNumberInternationalFallbackWidget,
            'address': forms.Textarea(attrs={'cols': '20', 'rows': '4'}),
            'avatar': ThumbnailFileInput
        }
        field_classes = {'username': UsernameField}


class UserCreationForm(BaseUserForm):
    password1 = forms.CharField(
        label="Passwort",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = True

    def save(self, commit=True):
        user = super().save()
        # set email as verified
        email_address = EmailAddress(
            user=user,
            email=user.email,
            verified=True,
            primary=True
        )
        email_address.save()
        return user



class UserChangeForm(BaseUserForm):
    password1 = forms.CharField(
        label="Passwort ändern",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Das alte Passwort kann nicht eingesehen werden. Aber es kann hier geändert werden.",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        if not self.request or not self.request.user.has_perm('users.change_permissions', self.instance):
            self.fields['role'].widget.attrs['readonly'] = True
            self.fields['janun_groups'].disabled = True
            self.fields['group_hats'].disabled = True
            self.fields['is_reviewed'].disabled = True
            self.helper.layout[-1].insert(
                0, HTML("""<p>Du kannst hier nichts ändern.<br>Bei Bedarf melde Dich (per E-Mail) bei uns.</p>"""),
            )
            # remove group_hats for Teamers:
            if self.request.user.role == 'TEAMER':
                self.fields['group_hats'] .widget = forms.HiddenInput()

    # return the instance value in case user is not allowed to edit role
    def clean_role(self):
        if not self.request or not self.request.user.has_perm('users.change_permissions', self.instance):
            return self.instance.role
        return self.cleaned_data['role']


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['placeholder'] = ""
        self.fields['login'].label = "Benutzername oder E-Mail-Adresse"
        self.fields['login'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['password'].widget.attrs['placeholder'] = ""
        self.fields['password'].widget.attrs['help_below'] = "True"
        self.fields['password'].help_text = """<a href="{}">Passwort vergessen?</a>""".format(
            reverse_lazy('account_reset_password')
        )


class UserSignupForm(SignupForm):
    name = forms.CharField(label="Voller Name")
    phone_number = PhoneNumberField(
        label="Telefonnummer", required=False, widget=PhoneNumberInternationalFallbackWidget,
        help_text="Damit wir Rückfragen zu Deinem Seminar zeitnah mit Dir klären können."
    )
    janun_groups = forms.ModelMultipleChoiceField(
        label="Gruppen-Mitgliedschaften",
        queryset=JANUNGroup.objects.all(),
        required=False,
        help_text="""Wähle die Gruppen aus, in denen Du Mitglied bist. Für mehrere, drücke <kbd>Strg</kbd>."""
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'name',
            'email',
            'username',
            'password1',
            'phone_number',
            'janun_groups',
        )
        if not self.errors:
            self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        self.fields['username'].label = "Benutzername"
        self.fields['username'].help_text = "Du kannst Dich übrigens auch mit Deiner E-Mail-Adresse anmelden."
        self.fields['username'].widget.attrs['autofocus'] = False
        self.fields['username'].widget.attrs['placeholder'] = ""

        self.fields['email'].widget.attrs['placeholder'] = ""
        self.fields['email'].help_text = "Die brauchen wir, um Dich zu Deinem Seminar zu kontaktieren."

        self.fields['password1'] = forms.CharField(
            label="Passwort",
            strip=False,
            widget=forms.PasswordInput(render_value=True),
            help_text="""Regeln: Min. 8 Zeichen, nicht nur Zahlen, nicht zu ähnlich zu Name oder E-Mail.<br>
                         <strong>Tipp:</strong> Probiere einen Satz, das lässt sich besser merken."""
        )

    def clean(self):
        # super().clean()
        dummy_user = User()
        dummy_user.username = self.cleaned_data.get("username")
        dummy_user.email = self.cleaned_data.get("email")
        dummy_user.name = self.cleaned_data.get("name")
        password = self.cleaned_data.get('password1')
        if password:
            try:
                get_adapter().clean_password(
                    password,
                    user=dummy_user)
            except forms.ValidationError as e:
                self.add_error('password1', e)
        return self.cleaned_data

    class Meta:
        widgets = {
            'avatar': ThumbnailFileInput
        }


class ResetPasswordKeyForm(forms.Form):

    password1 = SetPasswordField(label="Neues Passwort")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.temp_key = kwargs.pop("temp_key", None)
        super().__init__(*args, **kwargs)
        self.fields['password1'].user = self.user

    def save(self):
        get_adapter().set_password(self.user, self.cleaned_data["password1"])
