import django_tables2 as tables
from django_tables2.utils import A

from groups.models import JANUNGroup


class JANUNGroupTable(tables.Table):
    logo = tables.TemplateColumn(
        """{% if record.logo %}{% include "groups/_group_logo.html" with logo=record.logo size="40px" %}{% endif %}""",
        verbose_name=""
    )
    name = tables.LinkColumn('groups:detail', args=[A('pk')], attrs={'a': {'class': 'font-weight-bold'}})
    tnt_this_year = tables.Column(verbose_name="TNT (dieses Jahr)", attrs={'cell': {'class': 'text-right'}})
    funding_this_year = tables.Column(verbose_name="Förderung (dieses Jahr)", attrs={'cell': {'class': 'text-right'}})
    group_hats = tables.ManyToManyColumn(linkify_item=True)

    class Meta:
        model = JANUNGroup
        fields = [
            'logo', 'name', 'group_hats'
        ]
        attrs = {
            'class': 'table table-hover'
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "name"
