from django.urls import reverse
from django.test import TestCase

from backend.users.models import User
from backend.seminars.models import Seminar


class DashboardTestCase(TestCase):
    url = reverse("dashboard:dashboard")

    @classmethod
    def setUpTestData(cls):
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Willkommen, Admin Mustermann")


class GlobalHistoryTestCase(TestCase):
    url = reverse("dashboard:history")

    @classmethod
    def setUpTestData(cls):
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Letzte Änderungen")


class SearchTestCase(TestCase):
    url = reverse("dashboard:search")

    @classmethod
    def setUpTestData(cls):
        # staff:
        cls.staff = User(name="Staff Mustermann", username="teststaff")
        cls.staff.set_password("secret")
        cls.staff.is_superuser = True
        cls.staff.is_staff = True
        cls.staff.save()
        # seminars:
        cls.testseminar = Seminar(
            title="Test-Seminar", start_date="2019-05-05", end_date="2019-05-06"
        )
        cls.testseminar.save()
        cls.testseminar2 = Seminar(
            title="Test-2Seminar", start_date="2018-05-05", end_date="2018-05-06"
        )
        cls.testseminar2.save()

    def test_get(self):
        self.client.login(username="teststaff", password="secret")
        response = self.client.get(self.url + "?q=Muster")
        self.assertContains(response, "Suche")
        self.assertContains(response, "Staff Mustermann")

    def test_search_by_year(self):
        self.client.login(username="teststaff", password="secret")
        response = self.client.get(self.url + "?q=test 2019")
        self.assertContains(response, "Suche")
        self.assertContains(response, "Test-Seminar")
        self.assertNotContains(response, "Test-2Seminar")
