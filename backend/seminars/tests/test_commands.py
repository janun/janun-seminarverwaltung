import datetime

from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from django.core import mail
from django.core.management import call_command

from backend.seminars.models import Seminar
from backend.emails.models import EmailTemplate


class CheckSeminarsTestCase(TestCase):
    def test_check_deadline_expired(self):
        ago_150_days = (timezone.now() - datetime.timedelta(days=150)).date()
        Seminar.objects.create(
            title="expired",
            status="zugesagt",
            start_date=ago_150_days,
            end_date=ago_150_days,
        )
        EmailTemplate.objects.create(
            template_key="seminar_deadline_expired",
            to_template="test@example.com",
            subject_template="test",
            text_template="test",
        )
        call_command("check_seminars")
        self.assertEqual(len(mail.outbox), 1)

    @patch("django.utils.timezone.now")
    def test_check_deadline_soon(self, mock_timezone_now):
        mock_timezone_now.return_value = datetime.datetime(
            2019, 4, 5, tzinfo=datetime.timezone(datetime.timedelta(hours=2))
        )
        Seminar.objects.create(
            title="soon_expired",
            status="zugesagt",
            start_date=datetime.date(2019, 3, 1),
            end_date=datetime.date(2019, 3, 1),
        )
        EmailTemplate.objects.create(
            template_key="seminar_deadline_soon",
            to_template="test@example.com",
            subject_template="test",
            text_template="test",
        )
        call_command("check_seminars")
        self.assertEqual(len(mail.outbox), 1)

    @patch("django.utils.timezone.now")
    def test_check_seminar_occurred(self, mock_timezone_now):
        mock_timezone_now.return_value = datetime.datetime(
            2019, 3, 2, tzinfo=datetime.timezone(datetime.timedelta(hours=2))
        )
        Seminar.objects.create(
            title="occurred",
            status="zugesagt",
            start_date=datetime.date(2019, 3, 1),
            end_date=datetime.date(2019, 3, 1),
        )
        EmailTemplate.objects.create(
            template_key="seminar_occurred",
            to_template="test@example.com",
            subject_template="test",
            text_template="test",
        )
        call_command("check_seminars")
        self.assertEqual(len(mail.outbox), 1)
