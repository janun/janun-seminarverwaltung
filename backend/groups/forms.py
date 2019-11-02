from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from backend.utils import Fieldset

from .models import JANUNGroup


class GroupCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Fieldset("Name", Field("name", css_class="w-full")))

    class Meta:
        model = JANUNGroup
        fields = ("name",)
