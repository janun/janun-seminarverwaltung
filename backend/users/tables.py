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
        verbose_name="Mitgliedschaften",
        linkify_item=True,
        default="",
        attrs={"a": {"class": "whitespace-no-wrap"}},
    )
    group_hats = tables.ManyToManyColumn(
        verbose_name="Gruppen-Hüte",
        linkify_item=True,
        default="",
        attrs={"a": {"class": "whitespace-no-wrap"}},
    )
    is_active = ColoredBooleanColumn()
    is_reviewed = ColoredBooleanColumn()
    has_totp = ColoredBooleanColumn(verbose_name="2FA", orderable=False)
    action = tables.Column(verbose_name="", orderable=False, empty_values=())
    last_visit = tables.Column(default="nie")

    def render_action(self, record):
        html = (
            '<a title="E-Mail schreiben" class="p-3 text-gray-500 hover:text-gray-800" href="mailto:{}">'
            '<svg class="fill-current h-3 w-3" viewBox="0 0 20 20"><path d="M18 2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4c0-1.1.9-2 2-2h16zm-4.37 9.1L20 16v-2l-5.12-3.9L20 6V4l-10 8L0 4v2l5.12 4.1L0 14v2l6.37-4.9L10 14l3.63-2.9z"/></svg>'
            "</a>".format(record.email)
        )
        if record.telephone:
            html += (
                '<a title="Anrufen" class="p-3 text-gray-500 hover:text-gray-800" href="tel:{}">'
                '<svg class="fill-current h-3 w-3" viewBox="0 0 20 20"><path d="M20 18.35V19a1 1 0 0 1-1 1h-2A17 17 0 0 1 0 3V1a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v4c0 .56-.31 1.31-.7 1.7L3.16 8.84c1.52 3.6 4.4 6.48 8 8l2.12-2.12c.4-.4 1.15-.71 1.7-.71H19a1 1 0 0 1 .99 1v3.35z"/></svg>'
                "</a>".format(record.telephone)
            )
        return format_html('<div class="flex items-center">{}</div>'.format(html))

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
            "action",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        attrs = {"class": "js-data-link table-sticky"}
        order_by = "name"
        empty_text = "Keine Konten gefunden."
