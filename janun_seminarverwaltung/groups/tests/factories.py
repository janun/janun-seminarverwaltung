import factory

from groups.models import JANUNGroup


class JANUNGroupFactory(factory.DjangoModelFactory):
    name = "Test Gruppe"

    class Meta:
        model = JANUNGroup
