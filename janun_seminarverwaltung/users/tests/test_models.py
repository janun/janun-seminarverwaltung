from tests import TestCase
from seminars.tests.factories import SeminarFactory
from groups.tests.factories import JANUNGroupFactory



class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    # def test__str__(self):
    #     self.assertEqual(
    #         self.user.__str__(),
    #         "testuser",  # This is the default username for self.make_user()
    #     )

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), "/users/testuser/")


class TestGetSeminars(TestCase):
    # TODO

    def setUp(self):
        # self.group = JANUNGroupFactory.create()
        self.seminar1 = SeminarFactory.create(title="seminar1")
        # self.seminar2 = SeminarFactory.create(title="seminar2")
        # self.seminar3 = SeminarFactory.create(title="seminar3")

    def test_verwalter_can_see_all(self):
        verwalter = self.make_user(role='VERWALTER')
        with self.login(verwalter):
            self.assertQuerysetEqual(
                verwalter.get_seminars(),
                [repr(self.seminar1)]
            )
