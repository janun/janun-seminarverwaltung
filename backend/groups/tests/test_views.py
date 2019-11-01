from django.urls import reverse
from django.test import TestCase

from backend.users.models import User
from backend.groups.models import JANUNGroup


class JANUNGroupExportTestCase(TestCase):
    url = reverse("groups:export")

    @classmethod
    def setUpTestData(cls):
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # group:
        cls.testgroup = JANUNGroup(name="Test-Gruppe")
        cls.testgroup.save()

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(len(response.content.split(b"\n")), 3)
        self.assertContains(response, "Test Gruppe")
