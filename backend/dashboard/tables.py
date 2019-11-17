import json

from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter
from django.template import defaultfilters
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context

import django_tables2 as tables


def render_two_values(primary, secondary):
    return format_html(
        '<p class="whitespace-no-wrap">{}</p> '
        '<p class="whitespace-no-wrap text-xs text-gray-600 table-condensed-hidden">{}</p>',
        primary,
        secondary,
    )


def get_history_url(record):
    try:
        return record.instance.get_absolute_url()
    except ObjectDoesNotExist:
        return None


class HistoryTable(tables.Table):

    history_date = tables.Column(verbose_name="Wann", orderable=False)

    def render_history_date(self, record):
        value = record.history_date
        return render_two_values(
            NaturalTimeFormatter.string_for(value),
            defaultfilters.date(timezone.localtime(value), "d.m.Y H:i"),
        )

    history_user = tables.Column(verbose_name="Wer", orderable=False, linkify=True)

    def render_history_user(self, record):
        return record.history_user

    history_object = tables.Column(
        verbose_name="Was", orderable=False, linkify=get_history_url
    )

    def render_history_object(self, record):
        try:
            value = record.instance
        except ObjectDoesNotExist:
            value = record.history_object

        return defaultfilters.truncatechars(value, 70)

    history_change_reason = tables.Column(
        verbose_name="Änderungen", orderable=False, empty_values=()
    )

    def render_history_change_reason(self, record):
        if record.history_type == "+":
            if record._meta.model_name == "historicalseminarcomment":
                return "Kommentar: {}".format(
                    defaultfilters.truncatechars(record.text, 150)
                )
            return format_html("<em>erstellt</em>")

        if record.history_type == "-":
            return format_html("<em>gelöscht</em>")

        if not record.history_change_reason:
            return format_html("<em>nichts geändert</em>")

        def format_change(change):
            field = change["field"]  # TODO try to get field verbose name
            if not change["new"]:
                string = "{} gelöscht".format(field)
            elif not change["old"]:
                string = "{}: {}".format(
                    field, defaultfilters.truncatechars(change["new"], 20)
                )
            else:
                string = "{}: {} → {}".format(
                    field,
                    defaultfilters.truncatechars(change["old"], 15),
                    defaultfilters.truncatechars(change["new"], 15),
                )
            return format_html(
                '<li class="mr-2 whitespace-no-wrap">{}</li>'.format(string)
            )

        changes = map(format_change, json.loads(record.history_change_reason))
        return format_html("<ul>{}</ul>".format("".join(changes)))

    class Meta:
        template_name = "table.html"
        fields = [
            "history_date",
            "history_user",
            "history_object",
            "history_change_reason",
        ]
        attrs = {"class": "table-sticky"}
