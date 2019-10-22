import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError

from backend.seminars.models import Seminar, FundingRate
from backend.groups.models import JANUNGroup


# TODO: Test annotations

# TODO: Test querysets


class FundingTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_group = JANUNGroup(name="Test-Gruppe")
        cls.test_group.save()
        funding_rate = FundingRate(
            year=2019,
            group_rate=13.5,
            group_rate_one_day=8,
            single_rate=10,
            single_rate_one_day=8,
            single_limit_formula="=IF(B>=3,(B-3)*200+450,450)",
            single_limit=1000,
        )
        funding_rate.save()

    def test_single_one_day(self):
        self.assertEqual(
            Seminar(
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 5, 1),
                planned_training_days=1,
                planned_attendees_max=10,
            ).get_max_funding(),
            80,
        )

    def test_single_one_day_limit(self):
        self.assertEqual(
            Seminar(
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 5, 1),
                planned_training_days=1,
                planned_attendees_max=100,
            ).get_max_funding(),
            450,
        )

    def test_single_four_day_limit(self):
        self.assertEqual(
            Seminar(
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 5, 1),
                planned_training_days=4,
                planned_attendees_max=100,
            ).get_max_funding(),
            650,
        )

    def test_single_limit(self):
        self.assertEqual(
            Seminar(
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 5, 1),
                planned_training_days=10,
                planned_attendees_max=100,
            ).get_max_funding(),
            1000,
        )

    def test_group_one_day(self):
        self.assertEqual(
            Seminar(
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 5, 1),
                planned_training_days=1,
                planned_attendees_max=10,
                group=self.test_group,
            ).get_max_funding(),
            80,
        )

    def test_group_two_day(self):
        self.assertEqual(
            Seminar(
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 5, 1),
                planned_training_days=2,
                planned_attendees_max=10,
                group=self.test_group,
            ).get_max_funding(),
            270,
        )

    def test_group_big(self):
        self.assertEqual(
            Seminar(
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 5, 1),
                planned_training_days=2,
                planned_attendees_max=100,
                group=self.test_group,
            ).get_max_funding(),
            2700,
        )


class FundingRateModelTestCase(TestCase):
    def test_create(self):
        funding_rate = FundingRate(year=2019, group_rate=13, single_rate=8)
        funding_rate.save()

    def test_clean_fail(self):
        with self.assertRaises(ValidationError):
            funding_rate = FundingRate(
                year=2019, group_rate=13, single_rate=8, single_limit_formula="BLALBA"
            )
            funding_rate.clean()
        with self.assertRaises(ValidationError):
            funding_rate = FundingRate(
                year=2019, group_rate=13, single_rate=8, group_limit_formula="BLALBA"
            )
            funding_rate.clean()

    def test_clean_success(self):
        funding_rate = FundingRate(
            year=2019,
            group_rate=13,
            single_rate=8,
            single_limit_formula="=IF(B>=3,(B-3)*200+450,450)",
        )
        funding_rate.clean()
        funding_rate = FundingRate(
            year=2019,
            group_rate=13,
            single_rate=8,
            group_limit_formula="=IF(B>=3,(B-3)*200+450,450)",
        )
        funding_rate.clean()


class SeminarModelTestCase(TestCase):
    def test_create_seminar(self):
        seminar = Seminar(title="Test", start_date="2019-04-01", end_date="2019-04-01")
        seminar.save()

    def test_slug(self):
        seminar = Seminar(title="Testö", start_date="2019-04-01", end_date="2019-04-01")
        seminar.save()
        self.assertEqual(seminar.slug, "testoe")
        seminar = Seminar(title="Testö", start_date="2019-04-01", end_date="2019-04-01")
        seminar.save()
        self.assertEqual(seminar.slug, "testoe-2")

    def test_validation_end_date(self):
        with self.assertRaisesMessage(
            ValidationError, "Muss größer/gleich Start-Datum sein"
        ):
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 4, 2),
                end_date=datetime.date(2019, 4, 1),
            ).clean()

    def test_validation_end_time(self):
        with self.assertRaisesMessage(
            ValidationError, "Muss größer/gleich Start-Zeit sein"
        ):
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 4, 1),
                start_time="15:00",
                end_date=datetime.date(2019, 4, 1),
                end_time="14:00",
            ).clean()

    def test_validation_planned_training_days(self):
        with self.assertRaisesMessage(
            ValidationError, "Muss kleiner gleich 2 (Dauer des Seminars) sein"
        ):
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 4, 1),
                end_date=datetime.date(2019, 4, 2),
                planned_training_days=10,
            ).clean()
        Seminar(
            title="Test",
            start_date=datetime.date(2019, 4, 1),
            end_date=datetime.date(2019, 4, 2),
            planned_training_days=2,
        ).clean()

    def test_get_deadline(self):
        self.assertEqual(
            Seminar(title="Test", start_date=datetime.date(2019, 3, 1)).get_deadline(),
            datetime.date(2019, 4, 15),
        )
        self.assertEqual(
            Seminar(title="Test", start_date=datetime.date(2019, 6, 1)).get_deadline(),
            datetime.date(2019, 7, 15),
        )
        self.assertEqual(
            Seminar(title="Test", start_date=datetime.date(2019, 8, 2)).get_deadline(),
            datetime.date(2019, 10, 15),
        )
        self.assertEqual(
            Seminar(title="Test", start_date=datetime.date(2019, 11, 5)).get_deadline(),
            datetime.date(2020, 1, 15),
        )
