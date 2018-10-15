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
    groups = tables.ManyToManyColumn(
        accessor=A('get_groups'), linkify_item=True, verbose_name="Gruppen"
    )
    last_login = tables.TemplateColumn(
        """{% load humanize %}
        <time datetime="{{ value|date:'c' }}" title="{{ value|date:"DATETIME_FORMAT" }}">
            {{ value|naturaltime|default:"noch nie" }}
        </time>"""
    )

    class Meta:
        model = User
        fields = [
            'avatar', 'name', 'role', 'groups', 'last_login', 'is_active'
        ]
        attrs = {
            'class': 'table',
        }
        row_attrs = {
            'data-link': lambda record: record.get_absolute_url()
        }
        order_by = "name"
