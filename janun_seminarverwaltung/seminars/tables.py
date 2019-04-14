import django_tables2 as tables
from django_tables2.utils import A

from .models import Seminar


class SeminarTable(tables.Table):
    title = tables.Column(linkify=True, attrs={'td': {'class': 'primary-column'}})
    start_date = tables.DateColumn(verbose_name="Datum", format="d.m.y", attrs={'cell': {'class': 'text-right'}})
    created = tables.DateColumn(format="d.m.y", attrs={'cell': {'class': 'text-right'}})
    group = tables.Column(linkify=True)
    author = tables.Column(linkify=True)
    tnt = tables.Column(
        verbose_name="TNT", orderable=False,
        attrs={'cell': {'class': 'text-right'}}
    )
    funding = tables.TemplateColumn(
        """{{ record.funding|default:0|default_if_none:'?'|floatformat:2 }} €""",
        verbose_name="Förderung", orderable=False,
        attrs={'cell': {'class': 'text-right'}}
    )
    state = tables.TemplateColumn(
        """<span class="text-{{ record.get_state_color }}">{{ record.get_state_display }}</span>""",
    )

    class Meta:
        model = Seminar
        template_name = 'seminars/table.html'
        fields = [
            'title', 'start_date', 'group', 'author', 'state', 'tnt', 'funding', 'created'
        ]
        attrs = {
            'class': 'table'
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "-start_date"
        empty_text = "Leider keine Seminare vorhanden."
