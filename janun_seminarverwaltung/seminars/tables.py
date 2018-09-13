import django_tables2 as tables

from .models import Seminar


class SeminarTable(tables.Table):
    title = tables.Column(linkify=True)
    start = tables.DateColumn()
    created = tables.DateColumn()
    group = tables.Column(linkify=True)
    author = tables.Column(linkify=True)

    class Meta:
        model = Seminar
        # TODO: Förderbedarf, Teilnahmetage nach JFG
        fields = [
            'title', 'start', 'group', 'author', 'state', 'created'
        ]
        attrs = {
            'class': 'table'
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "start"
        empty_text = "Leider keine Seminare vorhanden."
