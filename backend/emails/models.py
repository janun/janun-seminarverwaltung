import os
from typing import Iterator

from django.db import models
from django.urls import reverse
from django.template import Template, Context
from django.core.mail import EmailMessage
from django.core import mail

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
        "Grundbedingung", max_length=255, choices=TEMPLATE_KEY_CHOICES,
    )
    description = models.CharField(
        "Beschreibung", max_length=255, blank=True, null=True
    )

    from_template = models.CharField(
        "Von", max_length=255, default="seminare@janun.de",
    )
    to_template = models.CharField(
        "An", max_length=255, default="{{ seminar.owner.email }}",
    )
    cc_template = models.CharField("CC", max_length=255, blank=True, null=True,)
    text_template = models.TextField("Text", blank=True, null=True)
    subject_template = models.CharField(
        "Betreff", max_length=255, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.template_key

    def get_absolute_url(self) -> str:
        return reverse("emails:update", kwargs={"pk": self.pk})

    def render(self, context, connection=None) -> EmailMessage:
        """render this email template using context"""
        # render templates
        from_email = render_template(self.from_template, context)
        to_email = render_template(self.to_template, context)
        cc = render_template(self.cc_template, context)
        subject = render_template(self.subject_template, context)
        body = render_template(self.text_template, context)

        # create mail
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to_email.split(","),
            cc=cc.split(","),
            connection=connection,
        )

        # attachments
        for attachment in self.attachments.all():
            filename = os.path.basename(attachment.file.name)
            email.attach(filename=filename, content=attachment.file.read())

        return email

    @classmethod
    def send(cls, template_key: str, context: dict):
        """Send mails using template

        Args:
            template_key: The name of the template
            context: Context to render the template with"""
        for email in cls.get_mails(template_key, context):
            email.send(fail_silently=False)

    @classmethod
    def get_mails(cls, template_key: str, context: dict) -> Iterator[EmailMessage]:
        """Generate mails using template

        Only gets mails for active templates and also evaluates conditions
        Creates one smtp connection for all found emails

        Args:
            template_key: The name of the template
            context: Context to render the template with
        Returns:
            Generator of EmailMessages
            """
        qs = cls.objects.filter(
            template_key=template_key, active=True
        ).prefetch_related("conditions")
        with mail.get_connection() as connection:
            for template_obj in qs:
                if all(
                    cond.evaluate(context) for cond in template_obj.conditions.all()
                ):
                    yield template_obj.render(context, connection=connection)

    class Meta:
        verbose_name = "E-Mail-Vorlage"
        verbose_name_plural = "E-Mail-Vorlagen"


class EmailAttachment(models.Model):
    template = models.ForeignKey(
        EmailTemplate, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField("Datei", upload_to="email_attachments/")

    class Meta:
        verbose_name = "E-Mail-Anhang"
        verbose_name_plural = "E-Mail-Anhänge"


class EmailTemplateCondition(models.Model):
    template = models.ForeignKey(
        EmailTemplate, on_delete=models.CASCADE, related_name="conditions"
    )
    expression = models.CharField(
        "Nebenbedingung", help_text="z.B. user.role == 'Teamer_in'", max_length=255,
    )

    def evaluate(self, context: dict) -> bool:
        expression = "{% if " + self.expression + " %}True{% endif %}"
        return render_template(expression, context) == "True"

    def __str__(self) -> str:
        return self.expression
