import django_tables2 as tables

from .models import Seminar


class SeminarTable(tables.Table):
    title = tables.Column(linkify=True, attrs={'td': {'class': 'font-weight-bold'}})
    start_date = tables.DateColumn(verbose_name="Datum", format="d.m.y", attrs={'cell': {'class': 'text-right'}})
    created = tables.DateColumn(format="d.m.y", attrs={'cell': {'class': 'text-right'}})
    group = tables.Column(linkify=True)
    author = tables.Column(linkify=True)
    state = tables.TemplateColumn(
        """<span class="badge badge-pill badge-{{ record.get_state_color }}">{{ record.get_state_display }}</span>"""
    )

    class Meta:
        model = Seminar
        # TODO: Förderbedarf, Teilnahmetage nach JFG
        fields = [
            'title', 'start_date', 'group', 'author', 'state', 'created'
        ]
        attrs = {
            'class': 'table table-hover'
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "-start_date"
        empty_text = "Leider keine Seminare vorhanden."
