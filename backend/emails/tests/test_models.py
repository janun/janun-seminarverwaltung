from django.test import TestCase
from django.core import mail

from backend.emails.models import EmailTemplate, EmailAttachment, EmailTemplateCondition


class SimpleEmailTestCase(TestCase):
    """Test basic functionality"""

    def setUp(self):
        # email template
        EmailTemplate(
            template_key="seminar_applied",
            from_template="seminare@janun.de",
            to_template="{{ email }}",
            subject_template="Test-Mail",
            text_template="Hallo, dies ist nur ein Test: {{ content }}",
        ).save()

    def test_mail_sent(self):
        EmailTemplate.send(
            "seminar_applied",
            {"email": "test@example.com", "content": "Test-Nachricht"},
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "test@example.com")
        self.assertIn("Test-Nachricht", mail.outbox[0].body)

    def test_silent_if_no_template(self):
        EmailTemplate.send(
            "testblabla", {"email": "test@example.com", "content": "Test-Nachricht"},
        )
        self.assertEqual(len(mail.outbox), 0)


class MultipleEmailTestCase(TestCase):
    """Tests that multiple mail are sent when there exist multiple template for one template key"""

    def setUp(self):
        # email template 1
        EmailTemplate(
            template_key="seminar_applied",
            from_template="seminare@janun.de",
            to_template="{{ email }}",
            subject_template="Test-Mail",
            text_template="Hallo, dies ist nur ein Test: {{ content }}",
        ).save()
        # email template 2
        EmailTemplate(
            template_key="seminar_applied",
            from_template="seminare@janun.de",
            to_template="seminare@janun.de",
            subject_template="Test-Mail",
            text_template="Hallo, dies ist nur ein Test: {{ content }}",
        ).save()

    def test_two_mails_sent(self):
        EmailTemplate.send(
            "seminar_applied",
            {"email": "test@example.com", "content": "Test-Nachricht"},
        )
        self.assertEqual(len(mail.outbox), 2)


class InactiveEmailTestCase(TestCase):
    """Tests that no email is sent, if email template is not active"""

    def setUp(self):
        # email template
        EmailTemplate(
            template_key="seminar_applied",
            from_template="seminare@janun.de",
            to_template="{{ email }}",
            subject_template="Test-Mail",
            text_template="Hallo, dies ist nur ein Test: {{ content }}",
            active=False,
        ).save()

    def test_no_mail_sent(self):
        EmailTemplate.send(
            "seminar_applied",
            {"email": "test@example.com", "content": "Test-Nachricht"},
        )
        self.assertEqual(len(mail.outbox), 0)


class ConditionTestCase(TestCase):
    """Tests with more conditions"""

    def setUp(self):
        # email template
        template = EmailTemplate(
            template_key="seminar_applied",
            from_template="seminare@janun.de",
            to_template="{{ email }}",
            subject_template="Test-Mail",
            text_template="Hallo, dies ist nur ein Test: {{ content }}",
        )
        template.save()
        EmailTemplateCondition(
            template=template, expression="""email == "foobar@example.com" """
        ).save()

    def test_no_mail_sent(self):
        EmailTemplate.send(
            "seminar_applied",
            {"email": "test@example.com", "content": "Test-Nachricht"},
        )
        self.assertEqual(len(mail.outbox), 0)


# class AttachmentsTestCase(TestCase):
#     """Tests wether email templates with attachments work"""

#     def setUp(self):
#         # email template
#         EmailTemplate(
#             template_key="seminar_applied",
#             from_template="seminare@janun.de",
#             to_template="{{ email }}",
#             subject_template="Test-Mail",
#             text_template="Hallo, dies ist nur ein Test: {{ content }}",
#             attachments=EmailAttachment(filename="Test-file",),
#         ).save()

#     def test_mail_sent_with_attachment(self):
#         EmailTemplate.send(
#             "seminar_applied",
#             {"email": "test@example.com", "content": "Test-Nachricht"},
#         )
#         self.assertEqual(len(mail.outbox), 0)
