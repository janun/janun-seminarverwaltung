import django_tables2 as tables
from django_tables2.utils import A

from janun_seminarverwaltung.users.models import User


class UserTable(tables.Table):
    avatar = tables.TemplateColumn(
        """
        {% if record.avatar %}
            <div class="round-image round-image--small">
                <img class="round-image__image" src="{{ record.avatar.url }}">
            </div>
        {% endif %}""",
        verbose_name="",
    )
    name = tables.Column(linkify=True)
    groups = tables.TemplateColumn(
        """{{ record.get_groups|join:"," }}""",
        verbose_name="Gruppen",
        orderable=False,
    )

    class Meta:
        model = User
        fields = [
            'avatar', 'name', 'role', 'groups'
        ]
        attrs = {
            'class': 'table',
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "name"
