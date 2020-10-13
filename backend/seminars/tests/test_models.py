import datetime
from unittest.mock import patch

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone


from backend.seminars.models import Seminar, FundingRate
from backend.groups.models import JANUNGroup


# TODO: Test annotations


class DeadlineAnnotationsTestCase(TestCase):
    def test_deadline(self):
        test1 = Seminar.objects.create(
            title="Test1",
            start_date=datetime.date(2019, 3, 1),
            end_date=datetime.date(2019, 3, 1),
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline().filter(
                deadline=datetime.date(2019, 4, 15)
            ),
            [repr(test1)],
        )

        test2 = Seminar.objects.create(
            title="Test2",
            start_date=datetime.date(2019, 6, 1),
            end_date=datetime.date(2019, 6, 1),
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline().filter(
                deadline=datetime.date(2019, 7, 15)
            ),
            [repr(test2)],
        )

        test3 = Seminar.objects.create(
            title="Test3",
            start_date=datetime.date(2019, 8, 2),
            end_date=datetime.date(2019, 8, 2),
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline().filter(
                deadline=datetime.date(2019, 10, 15)
            ),
            [repr(test3)],
        )

        test4 = Seminar.objects.create(
            title="Test4",
            start_date=datetime.date(2019, 11, 5),
            end_date=datetime.date(2019, 11, 5),
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline().filter(
                deadline=datetime.date(2020, 1, 15)
            ),
            [repr(test4)],
        )

        # goes over year boundary
        test5 = Seminar.objects.create(
            title="Test5",
            start_date=datetime.date(2019, 12, 31),
            end_date=datetime.date(2020, 1, 1),
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline().filter(
                deadline=datetime.date(2020, 1, 15)
            ),
            [repr(test5), repr(test4)],
        )

    def test_deadline_status_expired(self):
        ago_150_days = (timezone.now() - datetime.timedelta(days=150)).date()
        expired = Seminar.objects.create(
            title="expired",
            status="zugesagt",
            start_date=ago_150_days,
            end_date=ago_150_days,
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline_status().filter(
                deadline_status="expired"
            ),
            [repr(expired)],
        )

    @patch("django.utils.timezone.now")
    def test_deadline_status_soon(self, mock_timezone_now):
        mock_timezone_now.return_value = datetime.datetime(
            2019, 4, 5, tzinfo=datetime.timezone(datetime.timedelta(hours=2))
        )
        soon = Seminar.objects.create(
            title="soon",
            status="zugesagt",
            start_date=datetime.date(2019, 3, 1),
            end_date=datetime.date(2019, 3, 1),
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline_status().filter(deadline_status="soon"),
            [repr(soon)],
        )

    def test_deadline_status_not_soon(self):
        in_150_days = (timezone.now() + datetime.timedelta(days=150)).date()
        not_soon = Seminar.objects.create(
            title="not_soon",
            status="zugesagt",
            start_date=in_150_days,
            end_date=in_150_days,
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline_status().filter(
                deadline_status="not_soon"
            ),
            [repr(not_soon)],
        )

    def test_deadline_status_not_applicable(self):
        ago_150_days = (timezone.now() - datetime.timedelta(days=150)).date()
        not_applicable = Seminar.objects.create(
            title="not_applicable",
            status="überwiesen",
            start_date=ago_150_days,
            end_date=ago_150_days,
        )
        self.assertQuerysetEqual(
            Seminar.objects.annotate_deadline_status().filter(
                deadline_status="not_applicable"
            ),
            [repr(not_applicable)],
        )


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

    def test_validation_planned_attendees_max(self):
        with self.assertRaisesMessage(
            ValidationError, "Muss größer/gleich Minimal-Wert sein"
        ):
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 4, 1),
                end_date=datetime.date(2019, 4, 1),
                planned_attendees_min=20,
                planned_attendees_max=10,
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

    def test_multiple_validation_errors(self):
        with self.assertRaisesMessage(
            ValidationError, "Muss größer/gleich Minimal-Wert sein"
        ) and self.assertRaisesMessage(
            ValidationError, "Muss größer/gleich Start-Datum sein"
        ):
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 5, 1),
                end_date=datetime.date(2019, 4, 1),
                planned_attendees_min=20,
                planned_attendees_max=10,
            ).clean()

    def test_get_deadline(self):
        self.assertEqual(
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 3, 1),
                end_date=datetime.date(2019, 3, 1),
            ).get_deadline(),
            datetime.date(2019, 4, 15),
        )
        self.assertEqual(
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 6, 1),
                end_date=datetime.date(2019, 6, 1),
            ).get_deadline(),
            datetime.date(2019, 7, 15),
        )
        self.assertEqual(
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 8, 2),
                end_date=datetime.date(2019, 8, 2),
            ).get_deadline(),
            datetime.date(2019, 10, 15),
        )
        self.assertEqual(
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 11, 5),
                end_date=datetime.date(2019, 11, 5),
            ).get_deadline(),
            datetime.date(2020, 1, 15),
        )
        # goes over year boundary
        self.assertEqual(
            Seminar(
                title="Test",
                start_date=datetime.date(2019, 12, 30),
                end_date=datetime.date(2020, 1, 3),
            ).get_deadline(),
            datetime.date(2020, 1, 15),
        )

    def test_confirmed_at(self):
        """Test that confirmed_at is populated when status is changed to zugesagt"""
        seminar = Seminar(
            title="Test",
            start_date=datetime.date(2019, 4, 1),
            end_date=datetime.date(2019, 4, 1),
        )
        seminar.save()
        self.assertIsNone(seminar.confirmed_at)
        seminar.status = "zugesagt"
        seminar.save()
        self.assertIsNotNone(seminar.confirmed_at)
