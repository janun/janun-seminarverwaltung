import factory
from psycopg2.extras import NumericRange

from django.utils.dateparse import parse_date

from seminars.models import Seminar
from groups.tests.factories import JANUNGroupFactory


class SeminarFactory(factory.DjangoModelFactory):
    title = "Test Seminar"
    content = "This is a test."
    start_date = parse_date("2019-01-05")
    end_date = parse_date("2019-01-10")
    location = "Hannover"
    planned_training_days = 5
    planned_attendees = NumericRange(10, 20)
    requested_funding = 100
    group = factory.SubFactory(JANUNGroupFactory)

    class Meta:
        model = Seminar
