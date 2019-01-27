from import_export import fields, resources
# from import_export.widgets import FieldWidget

from janun_seminarverwaltung.users.models import User

from seminars.models import Seminar


class SeminarResource(resources.ModelResource):

    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        FieldWidget = cls.widget_from_django_field(django_field)
        widget_kwargs = cls.widget_kwargs_for_field(field_name)
        field = fields.Field(
            attribute=field_name, column_name=django_field.verbose_name,
            widget=FieldWidget(**widget_kwargs), readonly=readonly
        )
        return field

    class Meta:
        model = Seminar
