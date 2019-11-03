from django.urls import reverse
from django.test import TestCase

from backend.users.models import User
from backend.seminars.models import Seminar


class SeminarsExportTestCase(TestCase):
    url = reverse("seminars:export", kwargs={"year": 2019})

    @classmethod
    def setUpTestData(cls):
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # seminar:
        cls.testseminar = Seminar(
            title="Test-Seminar", start_date="2019-05-05", end_date="2019-05-06"
        )
        cls.testseminar.save()

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(len(response.content.split(b"\n")), 3)
        self.assertContains(response, "Test-Seminar")


# class SeminarImportViewTestCase(TestCase):
#     url = reverse("seminars:import")

#     @classmethod
#     def setUpTestData(cls):
#         cls.testuser = User(name="Max Mustermann", username="testuser")
#         cls.testuser.set_password("secret")
#         cls.testuser.save()
#         cls.testadmin = User(name="Admin Mustermann", username="testadmin")
#         cls.testadmin.set_password("secret")
#         cls.testadmin.is_staff = True
#         cls.testadmin.save()

#     def test_staff_required(self):
#         self.client.login(username="testuser", password="secret")
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 403)

#     def test_get(self):
#         self.client.login(username="testadmin", password="secret")
#         response = self.client.get(self.url)
#         self.assertContains(response, "Seminare importieren")

#     def test_post(self):
#         self.client.login(username="testadmin", password="secret")
#         with open("seminars.csv") as fp:
#             response = self.client.post({"file": fp})
#         self.assertContains(response, "Seminare importieren")


class SeminarDeleteViewTestCase(TestCase):
    url = reverse("seminars:delete", kwargs={"year": 2019, "slug": "test-seminar"})

    @classmethod
    def setUpTestData(cls):
        # teamer:
        cls.testteamer = User(name="Teamer Mustermann", username="testteamer")
        cls.testteamer.set_password("secret")
        cls.testteamer.save()
        # owner teamer:
        cls.testowner = User(name="Teamer Mustermann", username="testowner")
        cls.testowner.set_password("secret")
        cls.testowner.save()
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # seminar:
        cls.testseminar = Seminar(
            title="Test-Seminar",
            start_date="2019-05-05",
            end_date="2019-05-06",
            owner=cls.testowner,
        )
        cls.testseminar.save()

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Test-Seminar löschen")

    def test_normal_teamer_denied(self):
        self.client.login(username="testteamer", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_owner_allowed_if_angemeldet(self):
        self.client.login(username="testowner", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Test-Seminar löschen")
        self.testseminar.status = "zugesagt"
        self.testseminar.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, "/")
        self.assertContains(response, "Test-Seminar wurde gelöscht")
