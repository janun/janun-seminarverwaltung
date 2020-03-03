from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from backend.users.models import User
from backend.groups.models import JANUNGroup
from .models import Seminar


class SeminarResource(resources.ModelResource):
    owner = fields.Field(
        column_name="owner", attribute="owner", widget=ForeignKeyWidget(User, "name")
    )

    group = fields.Field(
        column_name="group",
        attribute="group",
        widget=ForeignKeyWidget(JANUNGroup, "name"),
    )

    class Meta:
        model = Seminar
        skip_unchanged = True
        clean_model_instances = True
