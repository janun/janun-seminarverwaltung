import datetime

from django.test import TestCase

from backend.api.models import Seminar


class SeminarTests(TestCase):
    def test_deadline(self):
        seminar = Seminar(title="Test Seminar", end_date=datetime.date(2018, 1, 1))
        self.assertEqual(seminar.deadline, datetime.date(2018, 4, 15))
