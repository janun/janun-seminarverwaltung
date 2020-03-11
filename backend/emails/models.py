import os

from django.db import models
from django.urls import reverse
from django.template import Template, Context
from django.core.mail import EmailMessage

from model_utils import Choices


def render_template(template: str, context: dict) -> str:
    if template is None:
        return ""
    template = "{% load janun %}" + template
    return Template(template).render(Context(context))


class EmailTemplate(models.Model):
    TEMPLATE_KEY_CHOICES = Choices(
        ("seminar_applied", "Seminar angemeldet"),
        ("seminar_delete", "Seminar gelöscht"),
        ("seminar_update", "Seminar geändert"),
        ("seminar_deadline_expired", "Seminar Abrechnungsfrist abgelaufen"),
        ("seminar_deadline_soon", "Seminar Abrechnungsfrist in 14 Tagen"),
        ("seminar_occurred", "Seminar stattgefunden (Enddatum Vergangenheit)"),
        ("user_signup", "Benutzer registriert"),
    )
    active = models.BooleanField("Aktiv", default=True)
    template_key = models.CharField(
        "Grundbedingung",
        help_text="Wann diese E-Mail verschickt werden soll",
        max_length=255,
        choices=TEMPLATE_KEY_CHOICES,
    )
    description = models.TextField("Beschreibung", blank=True, null=True)

    from_template = models.CharField(
        "Absender", max_length=255, default="seminare@janun.de",
    )
    to_template = models.CharField(
        "Empfänger",
        help_text="Mehrere durch Komma trennen",
        max_length=255,
        default="{{ seminar.owner.email }}",
    )
    cc_template = models.CharField(
        "CC-Kopie",
        help_text="Mehrere durch Komma trennen",
        max_length=255,
        blank=True,
        null=True,
    )
    text_template = models.TextField("Text", blank=True, null=True)
    subject_template = models.CharField(
        "Betreff", max_length=255, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.template_key

    def get_absolute_url(self) -> str:
        return reverse("emails:update", kwargs={"pk": self.pk})

    @classmethod
    def _send(cls, template_obj, context):
        if template_obj.active is False:
            return

        # evaluate conditions
        for condition in template_obj.conditions.all():
            if not condition.evaluate(context):
                return

        # render templates
        from_email = render_template(template_obj.from_template, context)
        to_email = render_template(template_obj.to_template, context)
        cc = render_template(template_obj.cc_template, context)
        subject = render_template(template_obj.subject_template, context)
        body = render_template(template_obj.text_template, context)

        # create mail
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to_email.split(","),
            cc=cc.split(","),
        )

        # attachments
        for attachment in template_obj.attachments.all():
            filename = attachment.filename
            if filename is None:
                filename = os.path.basename(attachment.file.name)
            email.attach(filename=filename, content=attachment.file.read())

        # actually send the mail
        email.send()

    @classmethod
    def send(cls, template_key: str, context: dict):
        """Send mails using template

        Args:
            template_key: The name of the template
            context: Context to render the template with"""
        qs = cls.objects.filter(template_key=template_key)
        for template_obj in qs:
            cls._send(template_obj, context)

    class Meta:
        verbose_name = "E-Mail-Vorlage"
        verbose_name_plural = "E-Mail-Vorlagen"


class EmailAttachment(models.Model):
    template = models.ForeignKey(
        EmailTemplate, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField("Datei", upload_to="email_attachments/")
    filename = models.CharField("Dateiname", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "E-Mail-Anhang"
        verbose_name_plural = "E-Mail-Anhänge"


class EmailTemplateCondition(models.Model):
    template = models.ForeignKey(
        EmailTemplate, on_delete=models.CASCADE, related_name="conditions"
    )
    expression = models.CharField("Bedingung", max_length=255,)

    def evaluate(self, context: dict) -> bool:
        expression = "{% if " + self.expression + " %}True{%endif%}"
        result = render_template(expression, context) == "True"
        return result
