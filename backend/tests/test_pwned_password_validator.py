from unittest import TestCase
from django.core.exceptions import ValidationError

from backend.validators import PwnedPasswordValidator


class PwnedPasswordValidatorTestCase(TestCase):
    def test_bad_password_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            PwnedPasswordValidator().validate("password123456")

    def test_good_password_passes(self):
        PwnedPasswordValidator().validate("aib3giNgoozae4")
