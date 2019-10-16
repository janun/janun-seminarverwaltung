from django.test import TestCase
from .models import Seminar


class SeminarTestCase(TestCase):
    def setUp(self):
        Seminar.objects.create(
            title="Test", start_date="2019-04-01", end_date="2019-04-01"
        )
        Seminar.objects.create(
            title="Test", start_date="2019-06-01", end_date="2019-06-01"
        )
