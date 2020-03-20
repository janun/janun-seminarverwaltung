from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from backend.utils import Fieldset, Formset

from .models import EmailTemplate, EmailAttachment, EmailTemplateCondition


AttachmentFormset = inlineformset_factory(
    EmailTemplate, EmailAttachment, fields=("file",), extra=1
)


class EmailTemplateConditionForm(forms.ModelForm):
    class Meta:
        model = EmailTemplateCondition
        fields = ("expression",)
        widgets = {"expression": forms.TextInput(attrs={"size": 64})}


ConditionFormset = inlineformset_factory(
    EmailTemplate, EmailTemplateCondition, form=EmailTemplateConditionForm, extra=1
)


class EmailTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset("", Field("description", css_class="w-full js-autogrow"),),
            Fieldset(
                "Bedingungen",
                Field("active", css_class=""),
                Field("template_key", css_class="w-full"),
                Formset("conditions"),
                text="""E-Mails werden verschickt, wenn die Vorlage aktiv ist
                und die Grundbedingung und alle Nebenbedingungen erfüllt sind.""",
            ),
            Fieldset(
                "E-Mail-Vorlage",
                Field("from_template", css_class="w-full"),
                Field("to_template", css_class="w-full"),
                Field("cc_template", css_class="w-full"),
                Field("subject_template", css_class="w-full"),
                Field("text_template", css_class="w-full js-autogrow"),
                text="""<p class="mb-4">In allen Feldern können Variablen benutzt werden.<br>
                Mögliche Variablen sind: <code>user</code> und ggf. <code>seminar</code>.<br>
                Bsp: <code>{{user.email}}</code>, <code>{{user.name}}</code>,
                <code>{{seminar.title}}</code>, <code>{{seminar.group.name}}</code></p>
                <p class="mb-4">Auch If-Abfragen sind möglich:<br>
                <code>{% if user.seminars.count < 2 %} Dein erstes Seminar {% endif %}</code>
                </p>
                <a class="underline" target="_blank"
                    href="https://docs.djangoproject.com/en/stable/ref/templates/language/">Mehr Infos</a>
                """,
            ),
            Fieldset("Anhänge", Formset("attachments")),
        )

    class Meta:
        model = EmailTemplate
        fields = (
            "template_key",
            "description",
            "active",
            "from_template",
            "to_template",
            "cc_template",
            "subject_template",
            "text_template",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }
