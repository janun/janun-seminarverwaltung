import datetime

from django.urls import reverse
from django.test import TestCase

from backend.users.models import User
from backend.groups.models import JANUNGroup
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


class SeminarStaffUpdateViewTestCase(TestCase):
    url = reverse(
        "seminars:detail_staff", kwargs={"year": 2019, "slug": "test-seminar"}
    )

    @classmethod
    def setUpTestData(cls):
        # teamer:
        cls.testteamer = User(name="Teamer Mustermann", username="testteamer")
        cls.testteamer.set_password("secret")
        cls.testteamer.save()
        # staff:
        cls.testadmin = User(name="Admin Mustermann", username="teststaff")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_staff = True
        cls.testadmin.save()
        # seminar:
        cls.testseminar = Seminar(
            title="Test-Seminar",
            start_date="2019-05-05",
            end_date="2019-05-06",
            owner=cls.testteamer,
        )
        cls.testseminar.save()

    def test_get(self):
        self.client.login(username="teststaff", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Test-Seminar")

    def test_teamer_denied(self):
        self.client.login(username="testteamer", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        self.client.login(username="teststaff", password="secret")
        response = self.client.post(
            self.url,
            {
                "title": "Test-Seminar",
                "start_date": "2019-05-05",
                "end_date": "2019-05-06",
                "status": "angemeldet",
            },
            follow=True,
        )
        self.assertContains(response, "Test-Seminar")
        self.assertContains(response, "Änderungen wurden gespeichert")


class SeminarTeamerUpdateViewTestCase(TestCase):
    url = reverse(
        "seminars:detail_teamer", kwargs={"year": 2019, "slug": "test-seminar"}
    )

    def setUp(self):
        # group:
        self.testgroup = JANUNGroup(name="Test-Gruppe")
        self.testgroup.save()
        self.testgroup2 = JANUNGroup(name="Test-Gruppe 2")
        self.testgroup2.save()
        # owner:
        self.testowner = User(name="Owner Mustermann", username="testowner")
        self.testowner.set_password("secret")
        self.testowner.save()
        self.testowner.janun_groups.set([self.testgroup])
        # arbitrary teamer:
        self.testadmin = User(name="Teamer Mustermann", username="testteamer")
        self.testadmin.set_password("secret")
        self.testadmin.save()
        # same group teamer:
        self.samegroup = User(
            name="Same Group Mustermann", username="samegroup", is_reviewed=True
        )
        self.samegroup.set_password("secret")
        self.samegroup.save()
        self.samegroup.janun_groups.set([self.testgroup])
        self.samegroup.save()
        # seminar:
        self.testseminar = Seminar(
            title="Test-Seminar",
            start_date="2019-05-05",
            end_date="2019-05-06",
            owner=self.testowner,
            group=self.testgroup,
        )
        self.testseminar.save()

    def test_get(self):
        self.client.login(username="testowner", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Test-Seminar")

    def test_teamer_denied(self):
        self.client.login(username="testteamer", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_same_group_allowed(self):
        self.client.login(username="samegroup", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Test-Seminar")

    def test_post(self):
        self.client.login(username="testowner", password="secret")
        response = self.client.post(
            self.url,
            {
                "title": "Test-Seminar",
                "start_date": "2019-05-05",
                "end_date": "2019-05-06",
                "status": "angemeldet",
            },
            follow=True,
        )
        self.assertContains(response, "Test-Seminar")
        self.assertContains(response, "Änderungen wurden gespeichert")

    def test_status_choices(self):
        self.client.login(username="testowner", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(
            response.context["form"].fields["status"].choices,
            [("angemeldet", "angemeldet"), ("abgesagt", "abgesagt")],
        )

    def test_group_choices(self):
        self.client.login(username="testowner", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(
            list(response.context["form"].fields["group"].choices),
            [("", "---------"), (1, "Test-Gruppe")],
        )

    def test_editing_disabled(self):
        self.testseminar.status = "zugesagt"
        self.testseminar.save()
        self.client.login(username="testowner", password="secret")
        response = self.client.post(
            self.url,
            {
                "title": "Foobar",
                "start_date": "2019-05-06",
                "end_date": "2019-05-06",
                "status": "zugesagt",
            },
            follow=True,
        )
        self.assertContains(response, "Test-Seminar")
        self.assertContains(response, "Änderungen wurden gespeichert")
        self.assertEqual(
            response.context["seminar"].start_date, datetime.date(2019, 5, 5)
        )
        self.assertEqual(response.context["seminar"].title, "Test-Seminar")

