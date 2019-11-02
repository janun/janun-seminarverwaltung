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
        self.assertContains(response, "Test-Gruppe")


class JANUNGroupCreateViewTestCase(TestCase):
    url = reverse("groups:add")

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
        self.assertContains(response, "Gruppe erstellen")

    def test_post(self):
        self.client.login(username="testadmin", password="secret")
        post_response = self.client.post(self.url, {"name": "Test-Gruppe"}, follow=True)
        self.assertRedirects(
            post_response, reverse("groups:detail", kwargs={"slug": "test-gruppe"})
        )
        self.assertContains(post_response, "Test-Gruppe")


class JANUNGroupDeleteViewTestCase(TestCase):
    url = reverse("groups:delete", kwargs={"slug": "test-gruppe"})

    @classmethod
    def setUpTestData(cls):
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # group
        cls.testgroup = JANUNGroup(name="Test-Gruppe")
        cls.testgroup.save()

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "wirklich löschen")

    def test_post(self):
        self.client.login(username="testadmin", password="secret")
        post_response = self.client.post(self.url, follow=True)
        self.assertRedirects(post_response, reverse("groups:staff_list"))
        self.assertContains(post_response, "Test-Gruppe wurde gelöscht")


class JANUNGroupUpdateViewTestCase(TestCase):
    url = reverse("groups:edit", kwargs={"slug": "test-gruppe"})

    @classmethod
    def setUpTestData(cls):
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # group
        cls.testgroup = JANUNGroup(name="Test-Gruppe")
        cls.testgroup.save()

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Test-Gruppe bearbeiten")

    def test_post(self):
        self.client.login(username="testadmin", password="secret")
        post_response = self.client.post(
            self.url, {"name": "Noch ne Test-Gruppe"}, follow=True
        )
        self.assertRedirects(
            post_response,
            reverse(
                "groups:detail", kwargs={"slug": "test-gruppe"}
            ),  # slug isnt changed
        )
        self.assertContains(post_response, "gespeichert")
        self.assertContains(post_response, "Noch ne Test-Gruppe")
