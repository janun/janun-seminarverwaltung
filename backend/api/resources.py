from import_export import resources
from . import models

class SeminarResource(resources.ModelResource):
    class Meta:
        model = models.Seminar
