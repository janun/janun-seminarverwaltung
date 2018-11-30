import requests
from requests.exceptions import RequestException
import hashlib

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


PWNED_ENDPOINT = 'https://api.pwnedpasswords.com/'
PWNED_PASSWORD_CHECK_PATH = 'range/'


class PwnedPasswordValidator(object):
    def _exists_as_pwned(self, password):
        try:
            hash = hashlib.sha1(password.encode("utf8")).hexdigest().upper()
            head, rest = hash[:5], hash[5:]
            url = PWNED_ENDPOINT + PWNED_PASSWORD_CHECK_PATH + head
            req = requests.get(url)
            return rest in req.content.decode('utf-8')
        except RequestException:
            return False

    def validate(self, password, *args, **kwargs):
        if self._exists_as_pwned(password):
            raise ValidationError(
                "Das Passwort wurde in einer Datenbank von gehackten Passwörtern gefunden."
            )

    def get_help_text(self):
        return "Es wird überprüft, ob das Passwort in einer Datenbank von gehackten Passwörtern enthalten ist."
