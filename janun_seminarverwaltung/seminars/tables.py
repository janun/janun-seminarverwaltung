import django_tables2 as tables

from .models import Seminar


class SeminarTable(tables.Table):
    title = tables.LinkColumn()
    start = tables.DateColumn(format="d.m.y")
    created = tables.DateColumn(format="d.m.y")
    group = tables.RelatedLinkColumn()
    author = tables.RelatedLinkColumn()

    class Meta:
        model = Seminar
        fields = [
            'title', 'start', 'group', 'author', 'state', 'created'
        ]
        attrs = {
            'class': 'table'
        }
        order_by = "start"
        empty_text = "Leider keine Seminare vorhanden."
