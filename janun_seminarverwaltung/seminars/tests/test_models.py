import factory
from psycopg2.extras import NumericRange

from django.utils.dateparse import parse_datetime

from tests import TestCase

from seminars.factory import SeminarFactory



class SeminarModelTest(TestCase):

    def setUp(self):
        self.seminar = SeminarFactory.build()

    def test_string_representation(self):
        self.assertEqual(
            self.seminar.__str__(),
            "Test Seminar"
        )

    def test_initial_state(self):
        self.assertEqual(
            self.seminar.state,
            "ANGEMELDET"
        )

    def test_validate_planned_training_days(self):
        s = SeminarFactory.build(planned_training_days=99)
        with self.assertValidationErrors(['planned_training_days']):
            s.full_clean()
        s.planned_training_days = 5
        s.full_clean()

    def test_validate_requested_funding(self):
        s = SeminarFactory.build(requested_funding=9999)
        with self.assertValidationErrors(['requested_funding']):
            s.full_clean()
        s.requested_funding = s.get_max_funding()
        s.full_clean()

    def test_end_after_start(self):
        s = SeminarFactory.build(end="2019-01-01 20:00")
        with self.assertValidationErrors(['end']):
            s.full_clean()
        s.end = "2019-01-10 20:00"
        s.full_clean()

    def test_multiple_validation_errors(self):
        s = SeminarFactory.build(
            requested_funding=99999,
            planned_training_days=99
        )
        with self.assertValidationErrors(['requested_funding', 'planned_training_days']):
            s.full_clean()

    def test_unique(self):
        s1 = SeminarFactory.create()  # TODO: factory create not working?
        s1.group.save()
        s1.save()
        s2 = SeminarFactory()
        self.assertIsNotNone(s1.pk)
        self.assertEqual(s1.title, s2.title)
        self.assertEqual(s1.start, s2.start)
        with self.assertValidationErrors(['title']):
            s2.full_clean()

    def test_get_max_funding(self):
        # mehrtägige Seminare für Gruppen
        self.assertEqual(
            SeminarFactory(planned_training_days=10, planned_attendees=NumericRange(10, 15))
            .get_max_funding(), 11.5 * 10 * 15
        )
        # eintägige Seminare für Gruppen
        self.assertEqual(
            SeminarFactory(planned_training_days=1, planned_attendees=NumericRange(10, 15))
            .get_max_funding(), 6.5 * 1 * 15
        )
        # mehrtägige Seminare ohne Gruppe
        self.assertEqual(
            SeminarFactory(planned_training_days=5, planned_attendees=NumericRange(10, 15), group=None)
            .get_max_funding(), 9 * 5 * 15
        )
        # mehrtägige Seminare ohne Gruppe; Obergrenze für 3 Tage
        self.assertEqual(
            SeminarFactory(planned_training_days=3, planned_attendees=NumericRange(10, 15), group=None)
            .get_max_funding(), 300
        )
        # mehrtägige Seminare ohne Gruppe; Obergrenze für 4 Tage
        self.assertEqual(
            SeminarFactory(planned_training_days=4, planned_attendees=NumericRange(10, 15), group=None)
            .get_max_funding(), 500
        )
        # mehrtägige Seminare ohne Gruppe; Obergrenze von 1000
        self.assertEqual(
            SeminarFactory(planned_training_days=99, planned_attendees=NumericRange(10, 99), group=None)
            .get_max_funding(), 1000
        )
        # eintägige Seminare ohne Gruppe
        self.assertEqual(
            SeminarFactory(planned_training_days=1, planned_attendees=NumericRange(10, 10), group=None)
            .get_max_funding(), 6.5 * 1 * 10
        )
        # Beispiel aus Seminarabrechnungsrichtlinie 2018
        s2 = SeminarFactory(planned_training_days=3, planned_attendees=NumericRange(10, 15))
        self.assertEqual(s2.get_max_funding(), 517.5)
        s2.group = None
        self.assertEqual(s2.get_max_funding(), 300)

    def test_get_deadline(self):
        self.assertEqual(
            SeminarFactory(end=parse_datetime("2018-01-01")).get_deadline(),
            parse_datetime("2018-04-15")
        )
        self.assertEqual(
            SeminarFactory(end=parse_datetime("2018-12-31")).get_deadline(),
            parse_datetime("2019-01-15")
        )
        self.assertEqual(
            SeminarFactory(end=parse_datetime("2018-05-15")).get_deadline(),
            parse_datetime("2019-07-15")
        )

    # def test_get_duration(self):
    #     self.fail()
