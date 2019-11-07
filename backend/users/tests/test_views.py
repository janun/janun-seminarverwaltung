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
        self.assertRedirects(post_response, reverse("dashboard:dashboard"))
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


class UserCreateViewTestCase(TestCase):
    url = reverse("users:add")

    @classmethod
    def setUpTestData(cls):
        # user:
        cls.testuser = User(name="Max Mustermann", username="testuser")
        cls.testuser.set_password("secret")
        cls.testuser.save()
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # group:
        cls.testgroup = JANUNGroup(name="Test-Gruppe")
        cls.testgroup.save()

    def test_superuser_required(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_create_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Neues Konto", status_code=200)

    def test_create_post(self):
        self.client.login(username="testadmin", password="secret")
        post_response = self.client.post(
            self.url,
            {
                "name": "Max Mustermann",
                "email": "max@mustermann.com",
                "telephone": "+495119897986",
                "username": "max",
                "password": "sadgadhe56egaefasdf",
                "is_active": True,
                "role": "Teamer_in",
                "janun_groups": 1,
            },
            follow=True,
        )
        self.assertRedirects(
            post_response, reverse("users:detail", kwargs={"username": "max"})
        )
        self.assertContains(post_response, "Max Mustermann")
        self.assertContains(post_response, "Konto erstellt")
        user = post_response.context["user"]
        self.assertEqual(user.name, "Max Mustermann")
        self.assertEqual(user.role, "Teamer_in")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.telephone, "+495119897986")
        self.assertEqual(user.janun_groups.get(), self.testgroup)


class UserDetailViewTestCase(TestCase):
    url = reverse("users:detail", kwargs={"username": "testuser"})

    @classmethod
    def setUpTestData(cls):
        # user:
        cls.testuser = User(name="Max Mustermann", username="testuser")
        cls.testuser.set_password("secret")
        cls.testuser.save()
        # staff:
        cls.testuser = User(name="Staff Mustermann", username="teststaff")
        cls.testuser.set_password("secret")
        cls.testuser.is_staff = True
        cls.testuser.save()
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # group:
        cls.testgroup = JANUNGroup(name="Test-Gruppe")
        cls.testgroup.save()

    def test_teamer_denied(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_detail_get(self):
        self.client.login(username="teststaff", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Max Mustermann", status_code=200)

    def test_detail_post(self):
        self.client.login(username="testadmin", password="secret")
        post_response = self.client.post(
            self.url,
            {
                "name": "Max Mustermann",
                "email": "max@mustermann.com",
                "telephone": "+495119897986",
                "username": "testuser",
                "password": "sadgadhe56egaefasdf",
                "is_active": True,
                "role": "Teamer_in",
                "janun_groups": 1,
            },
            follow=True,
        )
        self.assertRedirects(
            post_response, reverse("users:detail", kwargs={"username": "testuser"})
        )
        self.assertContains(post_response, "Max Mustermann")
        self.assertContains(post_response, "gespeichert")
        user = post_response.context["user"]
        self.assertEqual(user.name, "Max Mustermann")
        self.assertEqual(user.role, "Teamer_in")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.telephone, "+495119897986")
        self.assertEqual(user.janun_groups.get(), self.testgroup)


class UserProfileViewTestCase(TestCase):
    url = reverse("account_profile")

    @classmethod
    def setUpTestData(cls):
        # user:
        cls.testuser = User(name="Max Mustermann", username="testuser")
        cls.testuser.set_password("secret")
        cls.testuser.save()

    def test_detail_get(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Max Mustermann", status_code=200)

    def test_detail_post(self):
        self.client.login(username="testuser", password="secret")
        post_response = self.client.post(
            self.url,
            {
                "name": "Max Mustermann",
                "email": "max@mustermann.com",
                "telephone": "+495119897986",
                "username": "testuser",
                "password": "sadgadhe56egaefasdf",
            },
            follow=True,
        )
        self.assertRedirects(post_response, reverse("account_profile"))
        self.assertContains(post_response, "Max Mustermann")
        self.assertContains(post_response, "gespeichert")
        user = post_response.context["user"]
        self.assertEqual(user.name, "Max Mustermann")
        self.assertEqual(user.telephone, "+495119897986")


class UserExportTestCase(TestCase):
    url = reverse("users:export")

    @classmethod
    def setUpTestData(cls):
        # user:
        cls.testuser = User(name="Max Mustermann", username="testuser")
        cls.testuser.set_password("secret")
        cls.testuser.save()
        # staff:
        cls.testuser = User(name="Staff Mustermann", username="teststaff")
        cls.testuser.set_password("secret")
        cls.testuser.is_staff = True
        cls.testuser.save()
        # admin:
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_superuser = True
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # group:
        cls.testgroup = JANUNGroup(name="Test-Gruppe")
        cls.testgroup.save()

    def test_teamer_denied(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(len(response.content.split(b"\n")), 5)
        self.assertContains(response, "Max Mustermann")


# TODO: DeleteView

# TODO: Test 2FA views
