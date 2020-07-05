import datetime

from django.core import mail
from django.urls import reverse
from django.test import TestCase

from backend.users.models import User
from backend.groups.models import JANUNGroup
from backend.seminars.models import Seminar, FundingRate, SeminarComment
from backend.emails.models import EmailTemplate


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


class SeminarImportViewTestCase(TestCase):
    url = reverse("seminars:import")

    @classmethod
    def setUpTestData(cls):
        cls.testuser = User(name="Max Mustermann", username="testuser")
        cls.testuser.set_password("secret")
        cls.testuser.save()
        cls.testadmin = User(name="Admin Mustermann", username="testadmin")
        cls.testadmin.set_password("secret")
        cls.testadmin.is_staff = True
        cls.testadmin.save()

    def test_staff_required(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get(self):
        self.client.login(username="testadmin", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Seminare importieren")

    # def test_post(self):
    #     self.client.login(username="testadmin", password="secret")
    #     with open("seminars.csv") as fp:
    #         response = self.client.post({"file": fp})
    #     self.assertContains(response, "Seminare importieren")


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
            start_date=datetime.date(2019, 5, 5),
            end_date=datetime.date(2019, 5, 5),
            owner=cls.testowner,
        )
        cls.testseminar.save()
        # comment on seminar:
        SeminarComment.objects.create(text="Blabla", seminar=cls.testseminar)

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
            start_date=datetime.date(2019, 5, 5),
            end_date=datetime.date(2019, 5, 6),
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


class HistoryTestCase(TestCase):
    url = reverse("seminars:history", kwargs={"year": 2019, "slug": "test-seminar"})

    def setUp(self):
        # testuser:
        self.testuser = User(name="Max Mustermann", username="testuser")
        self.testuser.set_password("secret")
        self.testuser.is_staff = True
        self.testuser.save()
        # seminar:
        self.testseminar = Seminar(
            title="Test-Seminar", start_date="2019-05-05", end_date="2019-05-06"
        )
        self.testseminar.save()

    def test_get(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Änderungshistorie")
        self.assertContains(response, "Test-Seminar")


class CalcMaxFundingViewTestCase(TestCase):
    url = reverse("seminars:calc_max_funding")

    def setUp(self):
        # testuser:
        self.testuser = User(name="Max Mustermann", username="testuser")
        self.testuser.set_password("secret")
        self.testuser.save()
        # funding_rate:
        self.funding_rate = FundingRate(year=2019, group_rate=10, single_rate=8)
        self.funding_rate.save()

    def test_single_get(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url + "?year=2019&group=&days=2&attendees=20")
        self.assertContains(response, "320.00")

    def test_group_get(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url + "?year=2019&group=5&days=2&attendees=20")
        self.assertContains(response, "400.00")


class SeminarApplyViewTestCase(TestCase):
    url = reverse("seminars:apply")

    def setUp(self):
        # testuser:
        self.testuser = User(
            name="Max Mustermann", username="testuser", email="testuser@example.com"
        )
        self.testuser.set_password("secret")
        self.testuser.save()
        # funding_rate:
        self.funding_rate = FundingRate(year=2019, group_rate=10, single_rate=8)
        self.funding_rate.save()
        # form date
        self.form_data = {
            "title": "Foobar",
            "description": "Blabla",
            "start_date": "2019-05-06",
            "end_date": "2019-05-06",
            "planned_training_days": "1",
            "planned_attendees_min": "10",
            "planned_attendees_max": "20",
            "requested_funding": "100",
            "confirm_policy": True,
            "confirm_funding": True,
            "confirm_deadline": True,
        }
        # email template
        EmailTemplate(
            template_key="seminar_applied",
            from_template="seminare@janun.de",
            to_template=self.testuser.email,
            subject_template="Anmeldebestätigung",
            text_template="Hallo {{ user.name }}, {{ seminar.title }} wurde angemeldet",
        ).save()

    def test_get(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "anmelden")

    def test_post_success(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.post(self.url, self.form_data, follow=True)
        self.assertContains(response, "Foobar")
        self.assertContains(response, "Seminar erfolgreich angemeldet")
        seminar = response.context["seminar"]
        self.assertEqual(seminar.start_date, datetime.date(2019, 5, 6))
        self.assertEqual(seminar.title, "Foobar")
        self.assertEqual(seminar.owner, self.testuser)

    def test_mail_sent(self):
        self.client.login(username="testuser", password="secret")
        self.client.post(self.url, self.form_data, follow=True)
        # mail is sent to testuser:
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.testuser.email)
        self.assertIn(self.testuser.name, mail.outbox[0].body)
        self.assertIn(self.form_data["title"], mail.outbox[0].body)

    def test_funding_too_high(self):
        self.client.login(username="testuser", password="secret")
        form_data = self.form_data
        form_data["requested_funding"] = 1000
        response = self.client.post(self.url, form_data, follow=True)
        self.assertNotContains(response, "Seminar erfolgreich angemeldet")
        self.assertFormError(response, "form", "requested_funding", "Maximal 160,00 €")


class StaffSeminarListViewTestCase(TestCase):

    url_2019 = reverse("seminars:list_staff", kwargs={"year": 2019})
    url_2020 = reverse("seminars:list_staff", kwargs={"year": 2020})
    url_all = reverse("seminars:list_staff_all")

    @classmethod
    def setUpTestData(cls):
        # admin:
        cls.testuser = User(name="Staff Mustermann", username="teststaff")
        cls.testuser.set_password("secret")
        cls.testuser.is_staff = True
        cls.testuser.save()
        # seminar:
        cls.testseminar1 = Seminar(
            title="Test-Seminar 2019", start_date="2019-05-05", end_date="2019-05-06"
        )
        cls.testseminar1.save()
        cls.testseminar2 = Seminar(
            title="Test-Seminar 2020", start_date="2020-05-05", end_date="2019-05-06"
        )
        cls.testseminar2.save()

    def test_get(self):
        self.client.login(username="teststaff", password="secret")
        response = self.client.get(self.url_2019)
        self.assertContains(response, "Seminare 2019")
        self.assertContains(response, "Test-Seminar 2019")
        self.assertNotContains(response, "Test-Seminar 2020")

    def test_get_all(self):
        self.client.login(username="teststaff", password="secret")
        response = self.client.get(self.url_all)
        self.assertContains(response, "Seminare")
        self.assertContains(response, "Test-Seminar 2019")
        self.assertContains(response, "Test-Seminar 2020")

    def test_confirmed_aggregates(self):
        Seminar(
            title="Test",
            start_date="2019-05-05",
            end_date="2019-05-06",
            requested_funding=1000,
            status="zugesagt",
        ).save()
        Seminar(
            title="Test",
            start_date="2019-06-05",
            end_date="2019-06-06",
            requested_funding=2000,
            status="zugesagt",
        ).save()
        self.client.login(username="teststaff", password="secret")
        response = self.client.get(self.url_2019)
        self.assertEqual(response.context["confirmed_aggregates"]["funding_sum"], 3000)
        self.assertContains(response, "3 000,00")


class SeminarCreateViewTestCase(TestCase):
    url = reverse("seminars:create")

    def setUp(self):
        # testuser:
        self.testuser = User(
            name="Max Mustermann", username="testuser", email="testuser@example.com",
        )
        self.testuser.set_password("secret")
        self.testuser.save()
        # test staff user:
        self.staffuser = User(
            name="Staff Mustermann",
            username="staffuser",
            email="staffuser@example.com",
        )
        self.staffuser.set_password("secret")
        self.staffuser.is_staff = True
        self.staffuser.is_admin = True
        self.staffuser.save()
        # funding_rate:
        self.funding_rate = FundingRate(year=2019, group_rate=10, single_rate=8)
        self.funding_rate.save()
        # form date
        self.form_data = {
            "title": "Foobar",
            "description": "Blabla",
            "status": "angemeldet",
            "start_date": "2019-05-06",
            "end_date": "2019-05-06",
            "planned_training_days": "1",
            "planned_attendees_min": "10",
            "planned_attendees_max": "20",
            "requested_funding": "100",
        }

    def test_get_403(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Keine Berechtigung", status_code=403)

    def test_get(self):
        self.client.login(username="staffuser", password="secret")
        response = self.client.get(self.url)
        self.assertContains(response, "Neues Seminar erstellen")

    def test_post_success(self):
        self.client.login(username="staffuser", password="secret")
        response = self.client.post(self.url, self.form_data, follow=True)
        self.assertContains(response, "Foobar")
        self.assertContains(response, "Seminar erfolgreich erstellt.")
        seminar = response.context["seminar"]
        self.assertEqual(seminar.start_date, datetime.date(2019, 5, 6))
        self.assertEqual(seminar.title, "Foobar")
