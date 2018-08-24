from django.core import mail

from tests import TestCase

from .factories import SeminarFactory
from seminars.models import Seminar
from groups.tests.factories import JANUNGroupFactory


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

    def test_can_see_seminars_of_own_janun_groups(self):
        group = JANUNGroupFactory.create()
        user = self.make_user()
        user.janun_groups.add(group)
        user.save()
        seminar = SeminarFactory.create(title="Test Seminar", group=group)
        with self.login(user):
            response = self.get_check_200(self.url_name)
        self.assertResponseContains("Test Seminar")
        self.assertQuerysetEqual(response.context['seminar_list'], [repr(seminar)])

    def test_can_see_seminars_of_own_group_hats(self):
        group = JANUNGroupFactory.create()
        user = self.make_user(role="PRUEFER")
        user.group_hats.add(group)
        user.save()
        seminar = SeminarFactory.create(title="Test Seminar", group=group)
        with self.login(user):
            response = self.get_check_200(self.url_name)
        self.assertResponseContains("Test Seminar")
        self.assertQuerysetEqual(response.context['seminar_list'], [repr(seminar)])


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
    url_name = 'seminars:create'

    def setUp(self):
        self.user = self.make_user()

    def test_login_required(self):
        self.assertLoginRequired(self.url_name)

    def test_initial_call(self):
        with self.login(self.user):
            response = self.get(self.url_name)
            self.response_302()
            self.assertEqual(response.url, self.reverse('seminars:create_step', step='content'))
            self.get(response.url)
            self.response_200()

    wizard_step_data = (
        {
            'step': 'content',
            'title': "Test Seminar",
            'content': "Dies ist ein Test",
        },
        {
            'step': 'datetime',
            'start': "2021-01-01 12:00",
            'end': "2021-01-05 20:00",
        },
        {
            'step': 'location',
            'location': "Hannover",
        },
        {
            'step': 'group',
            'group': "",
        },
        {
            'step': 'days',
            'planned_training_days': "5",
        },
        {
            'step': 'attendees',
            'planned_attendees_0': "10",
            'planned_attendees_1': "20",
        },
        {
            'step': 'funding',
            'requested_funding': "10",
        },
        {
            'step': 'barriers',
            'mobility_barriers': "",
            'language_barriers': "",
            'hearing_barriers': "",
            'seeing_barriers': "",
        },
        {
            'step': 'confirm',
            'confirm_policy': True,
            'confirm_deadline': True,
            'confirm_funding': True
        },
    )

    def test_all_steps(self):
        self.make_user("Verwalter", role="VERWALTER")
        with self.login(self.user):
            first_step = self.wizard_step_data[0]['step']
            self.get('seminars:create_step', step=first_step)
            self.response_200()

            for step_data in self.wizard_step_data:
                step = step_data.pop('step')
                data = {'seminar_wizard_view-current_step': step}
                for key, value in step_data.items():
                    data["{0}-{1}".format(step, key)] = value
                post_response = self.post('seminars:create_step', data=data, step=step)
                self.response_302()
                get_response = self.get(post_response.url)
                self.response_200()
            self.assertEqual(post_response.url, self.reverse('seminars:create_step', step='done'))
            # sends mail to author and verwalter
            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(mail.outbox[0].subject, 'Dein Seminar "Test Seminar"')
            self.assertEqual(mail.outbox[1].subject, 'Neues Seminar "Test Seminar"')





class SeminarUpdateViewTests(TestCase):
    pass
