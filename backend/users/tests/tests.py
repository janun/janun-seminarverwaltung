from django.urls import reverse
from django.test import TestCase

from backend.users.models import User
from backend.groups.models import JANUNGroup


class LoginTestCase(TestCase):
    url = reverse("account_login")

    @classmethod
    def setUpTestData(cls):
        cls.testuser = User(name="Max Mustermann", username="testuser")
        cls.testuser.set_password("secret")
        cls.testuser.save()

    def test_login_get(self):
        get_response = self.client.get(self.url)
        self.assertContains(get_response, "Anmelden")

    def test_login_post_success(self):
        post_response = self.client.post(
            self.url, {"login": "testuser", "password": "secret"}, follow=True
        )
        self.assertRedirects(post_response, reverse("dashboard"))
        self.assertContains(post_response, "Willkommen, Max Mustermann")

    def test_login_post_failure(self):
        post_response = self.client.post(
            self.url, {"login": "foobar", "password": "blablabla"}
        )
        self.assertContains(
            post_response, "Der Anmeldename und/oder das Passwort sind leider falsch."
        )


class SingupTestCase(TestCase):
    url = reverse("account_signup")

    @classmethod
    def setUpTestData(cls):
        cls.testgroup = JANUNGroup(name="Test-Gruppe")
        cls.testgroup.save()

    def test_signup_get(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Neues Konto Anlegen", status_code=200)

    def test_signup_post(self):
        post_response = self.client.post(
            self.url,
            {
                "name": "Max Mustermann",
                "email": "max@mustermann.com",
                "telephone": "+495119897986",
                "username": "max",
                "password1": "sadgadhe56egaefasdf",
                "password2": "sadgadhe56egaefasdf",
                "janun_groups": "1",
                "data_protection_read": "on",
            },
            follow=True,
        )
        self.assertRedirects(post_response, "/")
        self.assertContains(post_response, "Willkommen, Max Mustermann")
        user = post_response.context["user"]
        self.assertEqual(user.name, "Max Mustermann")
        self.assertEqual(user.telephone, "+495119897986")
        self.assertEqual(user.janun_groups.get(), self.testgroup)
