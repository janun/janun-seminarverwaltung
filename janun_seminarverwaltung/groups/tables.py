import django_tables2 as tables
from django_tables2.utils import A

from groups.models import JANUNGroup


class JANUNGroupTable(tables.Table):
    logo = tables.TemplateColumn(
        """
        {% if record.logo %}
            <div class="round-image round-image--small round-image--logo">
                <img class="round-image__image" src="{{ record.logo.url }}">
            </div>
        {% endif %}""",
        verbose_name=""
    )
    name = tables.LinkColumn('groups:detail', args=[A('pk')])
    group_hats = tables.ManyToManyColumn(linkify_item=True)

    class Meta:
        model = JANUNGroup
        fields = [
            'logo', 'name', 'group_hats'
        ]
        attrs = {
            'class': 'table'
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "name"
