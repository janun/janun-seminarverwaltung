from tests import TestCase

from .factories import SeminarFactory
from seminars.models import Seminar


class SeminarListViewTests(TestCase):
    url_name = 'seminars:list'

    def test_login_required(self):
        self.assertLoginRequired(self.url_name)

    def test_no_seminars(self):
        with self.login(self.make_user()):
            response = self.assertGoodView(self.url_name)
        self.assertResponseContains("Leider keine Seminare vorhanden.")
        self.assertQuerysetEqual(response.context['seminar_list'], [])

    def test_can_see_own_seminars(self):
        user = self.make_user()
        seminar = SeminarFactory.create(title="Test Seminar", author=user)
        with self.login(user):
            response = self.get_check_200(self.url_name)
        self.assertResponseContains("Test Seminar")
        self.assertQuerysetEqual(response.context['seminar_list'], [repr(seminar)])

    def test_does_not_see_others_seminars(self):
        user = self.make_user()
        user2 = self.make_user("user2")
        SeminarFactory.create(title="Test Seminar", author=user2)
        with self.login(user):
            response = self.get_check_200(self.url_name)
        self.assertResponseNotContains("Test Seminar")
        self.assertResponseContains("Leider keine Seminare vorhanden.")
        self.assertQuerysetEqual(response.context['seminar_list'], [])


class SeminarDetailViewTests(TestCase):
    url_name = 'seminars:detail'

    def setUp(self):
        self.user = self.make_user()
        self.seminar = SeminarFactory.create(title="Test Seminar", author=self.user)

    def test_login_required(self):
        self.assertLoginRequired(self.url_name, pk=self.seminar.pk)

    def test_not_found(self):
        with self.login(self.user):
            self.get(self.url_name, pk=987)
        self.response_404()

    def test_can_see_own_seminar(self):
        with self.login(self.user):
            response = self.get_check_200(self.url_name, pk=self.seminar.pk)
        self.assertResponseContains("Test Seminar")
        self.assertEqual(response.context['object'], self.seminar)

    def test_cannot_see_others_seminar(self):
        user2 = self.make_user("user2")
        with self.login(user2):
            self.get(self.url_name, pk=self.seminar.pk)
        self.response_403()

    def test_verwalter_can_see_other_seminars(self):
        verwalter = self.make_user("user2", role="VERWALTER")
        with self.login(verwalter):
            response = self.get_check_200(self.url_name, pk=self.seminar.pk)
        self.assertResponseContains("Test Seminar")
        self.assertEqual(response.context['object'], self.seminar)


class SeminarDeleteViewTests(TestCase):
    url_name = 'seminars:delete'

    def setUp(self):
        self.user = self.make_user()
        self.seminar = SeminarFactory.create(title="Test Seminar", author=self.user)

    def test_login_required(self):
        self.assertLoginRequired(self.url_name, pk=self.seminar.pk)

    def test_not_found(self):
        with self.login(self.user):
            self.get(self.url_name, pk=987)
        self.response_404()

    def test_cannot_delete_others_seminar(self):
        user2 = self.make_user("user2")
        with self.login(user2):
            self.get(self.url_name, pk=self.seminar.pk)
        self.response_403()

    def test_can_delete_own_seminar(self):
        with self.login(self.user):
            self.post(self.url_name, pk=self.seminar.pk)
        self.response_302()
        self.assertFalse(Seminar.objects.filter(pk=self.seminar.pk).exists())

    def test_verwalter_can_delete_others_seminar(self):
        verwalter = self.make_user("user2", role="VERWALTER")
        with self.login(verwalter):
            self.post(self.url_name, pk=self.seminar.pk)
        self.response_302()
        self.assertFalse(Seminar.objects.filter(pk=self.seminar.pk).exists())


class SeminarWizardViewTests(TestCase):
    pass


class SeminarUpdateViewTests(TestCase):
    pass
