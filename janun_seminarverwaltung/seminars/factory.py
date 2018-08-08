import factory
from psycopg2.extras import NumericRange

from django.utils.dateparse import parse_datetime

from .models import Seminar
from groups.factory import JANUNGroupFactory


class SeminarFactory(factory.Factory):
    title = "Test Seminar"
    content = "This is a test."
    start = parse_datetime("2019-01-05 12:00")
    end = parse_datetime("2019-01-10 20:00")
    location = "Hannover"
    planned_training_days = 5
    planned_attendees = NumericRange(10, 20)
    requested_funding = 100
    group = factory.SubFactory(JANUNGroupFactory)

    class Meta:
        model = Seminar
