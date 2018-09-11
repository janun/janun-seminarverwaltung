import django_tables2 as tables
from django_tables2.utils import A

from groups.models import JANUNGroup


class JANUNGroupTable(tables.Table):
    logo = tables.TemplateColumn(
        """
        {% if record.logo %}
            <div class="image-button"><img class="image-button__image" src="{{ record.logo.url }}"></div>
        {% endif %}""",
        verbose_name=""
    )
    name = tables.LinkColumn('groups:detail', args=[A('pk')])
    group_hats = tables.ManyToManyColumn()

    class Meta:
        model = JANUNGroup
        fields = [
            'logo', 'name', 'group_hats'
        ]
        attrs = {
            'class': 'table'
        }
        order_by = "name"
