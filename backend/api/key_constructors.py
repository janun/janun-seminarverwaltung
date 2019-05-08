import datetime

from django.core.cache import cache
from django.utils.encoding import force_text
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    RetrieveSqlQueryKeyBit,
    UserKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class UpdatedAtKeyBit(KeyBitBase):
    def get_data(self, **kwargs):
        key = "api_updated_at_timestamp"
        value = cache.get(key, None)
        if not value:
            value = datetime.datetime.utcnow()
            cache.set(key, value=value)
        return force_text(value)


class CustomObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()
    user = UserKeyBit()


CustomObjectKeyFunction = CustomObjectKeyConstructor()


class CustomListKeyConstructor(DefaultKeyConstructor):
    updated_at = UpdatedAtKeyBit()
    user = UserKeyBit()


CustomListKeyFunction = CustomListKeyConstructor()
