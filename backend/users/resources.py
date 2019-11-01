from import_export import fields, resources
from import_export.widgets import ManyToManyWidget

from backend.users.models import User
from backend.groups.models import JANUNGroup


class UserResource(resources.ModelResource):
    janun_groups = fields.Field(
        column_name="janun_groups",
        attribute="janun_groups",
        widget=ManyToManyWidget(JANUNGroup, field="name"),
    )

    group_hats = fields.Field(
        column_name="group_hats",
        attribute="group_hats",
        widget=ManyToManyWidget(JANUNGroup, field="name"),
    )

    class Meta:
        model = User
