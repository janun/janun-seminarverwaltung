import django_tables2 as tables

from backend.utils import ColoredBooleanColumn
from .models import EmailTemplate


class EmailTemplateTable(tables.Table):
    active = ColoredBooleanColumn()
    description = tables.Column(linkify=True, attrs={"td": {"class": "primary-column"}})

    class Meta:
        model = EmailTemplate
        template_name = "table.html"
        fields = [
            "active",
            "description",
            "template_key",
            "to_template",
            "subject_template",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        attrs = {"class": "js-row-link table-sticky"}
        order_by = "template_key"
        empty_text = "Keine E-Mail-Vorlagen gefunden."
