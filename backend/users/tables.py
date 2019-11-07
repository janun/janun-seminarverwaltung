from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter
from django.template import defaultfilters
from django.utils import timezone


import django_tables2 as tables

from backend.utils import ColoredBooleanColumn
from .models import User


class UserTable(tables.Table):
    name = tables.Column(
        verbose_name="Name", linkify=True, attrs={"td": {"class": "primary-column"}}
    )
    janun_groups = tables.ManyToManyColumn(
        verbose_name="Mitgliedschaften", linkify_item=True, default=""
    )
    group_hats = tables.ManyToManyColumn(
        verbose_name="Gruppen-Hüte", linkify_item=True, default=""
    )
    is_active = ColoredBooleanColumn()
    is_reviewed = ColoredBooleanColumn()
    has_totp = ColoredBooleanColumn(verbose_name="2FA", orderable=False)

    def render_name(self, record):
        return format_html(
            '<p class="whitespace-no-wrap">{}</p>'
            '<p class="whitespace-no-wrap text-xs text-gray-600 font-normal">{}</p>',
            record.name,
            record.username,
        )

    def render_last_visit(self, record, value):
        return format_html(
            '<p class="whitespace-no-wrap">{}</p>'
            '<p class="whitespace-no-wrap text-xs text-gray-600 font-normal">{}</p>',
            NaturalTimeFormatter.string_for(value),
            defaultfilters.date(timezone.localtime(value), "d.m.Y H:i"),
        )

    class Meta:
        model = User
        template_name = "table.html"
        fields = [
            "name",
            "role",
            "janun_groups",
            "group_hats",
            "is_active",
            "is_reviewed",
            "has_totp",
            "last_visit",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        attrs = {"class": "js-data-link table-hover"}
        order_by = "name"
        empty_text = "Keine Konten gefunden."
