import json

from django.utils.html import format_html, escape, mark_safe
from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter
from django.template import defaultfilters
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

import django_tables2 as tables

from backend.seminars.templatetags.janun import highlight


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
            value = str(record.history_object)
            if not value:
                value = record.name  # workaround for strange User.__str__ behaviour

        return render_two_values(
            truncatechars(value, 70), record.history_object._meta.verbose_name,
        )

    history_change_reason = tables.Column(
        verbose_name="Änderungen", orderable=False, empty_values=()
    )

    def render_history_change_reason(self, record):
        if record.history_type == "+":
            if record._meta.model_name == "historicalseminarcomment":
                return "Kommentar: {}".format(truncatechars(record.text, 150))
            return format_html("<em>erstellt</em>")

        if record.history_type == "-":
            return format_html("<em>gelöscht</em>")

        if not record.history_change_reason:
            return format_html("<em>nichts geändert</em>")

        def format_change(change):
            # get field name
            try:
                field = record.instance._meta.get_field(change["field"]).verbose_name
            except FieldDoesNotExist:
                field = change["field"]

            new = truncatechars(change["new"], 15)
            old = truncatechars(change["old"], 15)

            if not change["new"]:  # was deleted
                string = f"{field} gelöscht"
            elif not change["old"]:  # is new
                string = f"{field}: {new}"
            else:  # was changed
                string = f"{field}: {old} → {new}"
            return f'<li class="mr-2 whitespace-no-wrap">{escape(string)}</li>'

        changes = map(format_change, json.loads(record.history_change_reason))
        return mark_safe(f"<ul>{''.join(changes)}</ul>")

    class Meta:
        template_name = "table.html"
        fields = [
            "history_date",
            "history_user",
            "history_object",
            "history_change_reason",
        ]
        attrs = {"class": "table-sticky"}


class SearchResultsTable(tables.Table):
    def __init__(self, *args, q="", **kwargs):
        self.q = q
        super().__init__(*args, **kwargs)

    name = tables.Column(
        verbose_name="Bezeichnung", orderable=False, linkify=False, empty_values=()
    )
    type = tables.Column(
        verbose_name="Typ", orderable=False, linkify=False, empty_values=()
    )

    def render_name(self, record):
        return highlight(str(record), self.q)

    def render_type(self, record):
        if record._meta.verbose_name == "Seminar":
            return "Seminar {}".format(record.start_date.year)
        return record._meta.verbose_name

    class Meta:
        template_name = "table.html"
        fields = ["name", "type"]
        attrs = {"class": "table-sticky js-row-link"}
        empty_text = "Keine Suchergebnisse."
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
