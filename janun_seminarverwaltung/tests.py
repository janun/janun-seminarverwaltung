from contextlib import contextmanager

from test_plus.test import TestCase as PlusTestCase
from django.core.exceptions import ValidationError


class ValidationErrorTestMixin(object):

    @contextmanager
    def assertValidationErrors(self, fields):
        """
        Assert that a validation error is raised, containing all the specified
        fields, and only the specified fields.
        """
        try:
            yield
            raise AssertionError("ValidationError not raised")
        except ValidationError as e:
            self.assertEqual(set(fields), set(e.message_dict.keys()))


class TestCase(ValidationErrorTestMixin, PlusTestCase):

    def make_user(self, username='testuser', password='password', perms=None, role=None):
        user = super().make_user(username, password, perms)
        if role:
            user.role = role
            user.save()
        return user
