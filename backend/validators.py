import hashlib
import requests
from requests.exceptions import RequestException
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.utils.html import mark_safe


PWNED_ENDPOINT = "https://api.pwnedpasswords.com/range/"


class PwnedPasswordValidator(object):
    """Checks pwnedpasswords.com, falls back to CommonPasswordValidator"""

    def _is_pwned(self, password):
        try:
            pw_hash = hashlib.sha1(password.encode("utf8")).hexdigest().upper()
            head, rest = pw_hash[:5], pw_hash[5:]
            url = PWNED_ENDPOINT + head
            req = requests.get(url)
            return rest in req.content.decode("utf-8")
        except RequestException:
            return None

    def validate(self, password, user=None):
        is_owned = self._is_pwned(password)
        if is_owned is None:
            CommonPasswordValidator().validate(password, user)
        elif is_owned is True:
            raise ValidationError(
                mark_safe(
                    "Wurde in einer "
                    '<a target="_blank" class="underline"'
                    'href="https://haveibeenpwned.com/Passwords">'
                    "Datenbank von gehackten Passwörtern</a> "
                    "gefunden."
                )
            )

    def get_help_text(self):
        return "Es wird überprüft, ob das Passwort in einer Datenbank von gehackten Passwörtern enthalten ist."
