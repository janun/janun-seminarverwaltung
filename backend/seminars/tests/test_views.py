from django.urls import reverse
from django.test import TestCase

from backend.users.models import User
from backend.seminars.models import Seminar


class JANUNGroupExportTestCase(TestCase):
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
