from unittest import TestCase
from django.core.exceptions import ValidationError

from backend.validators import PwnedPasswordValidator


class PwnedPasswordValidatorTestCase(TestCase):
    def test_raises(self):
        with self.assertRaises(ValidationError):
            PwnedPasswordValidator().validate("password123456")
