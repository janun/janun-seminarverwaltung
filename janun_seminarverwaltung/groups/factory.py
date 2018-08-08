import factory

from .models import JANUNGroup


class JANUNGroupFactory(factory.Factory):
    name = "Test Gruppe"

    class Meta:
        model = JANUNGroup
