import django_tables2 as tables

from .models import Seminar


class SeminarTable(tables.Table):
    title = tables.Column(linkify=True)
    start_date = tables.DateColumn(verbose_name="Datum", format="D, d.m.y")
    created = tables.DateColumn()
    group = tables.Column(linkify=True)
    author = tables.Column(linkify=True)

    class Meta:
        model = Seminar
        # TODO: Förderbedarf, Teilnahmetage nach JFG
        fields = [
            'title', 'start_date', 'group', 'author', 'state', 'created'
        ]
        attrs = {
            'class': 'table panel'
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "-start_date"
        empty_text = "Leider keine Seminare vorhanden."
