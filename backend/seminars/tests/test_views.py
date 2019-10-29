from django.urls import reverse
from django.test import TestCase

from backend.users.models import User


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
