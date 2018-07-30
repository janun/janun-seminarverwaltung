import django_tables2 as tables
from django_tables2.utils import A

from .models import Seminar


class SeminarTable(tables.Table):
    title = tables.LinkColumn()
    start = tables.DateColumn(format="d.m.y")
    created = tables.DateColumn(format="d.m.y")
    group = tables.RelatedLinkColumn()
    author = tables.RelatedLinkColumn()

    class Meta:
        model = Seminar
        # template_name = 'seminars/_table.html'
        fields = [
            'title', 'start', 'group', 'author', 'state', 'created'
        ]
        attrs = {
            'class': 'table'
        }
        order_by = "start"
