from import_export import resources

from .models import JANUNGroup


class JANUNGroupResource(resources.ModelResource):
    class Meta:
        model = JANUNGroup
