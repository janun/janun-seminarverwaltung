from django.utils.html import format_html
from django.template import defaultfilters

import django_tables2 as tables

from backend.utils import NumericColumn, EuroColumn
from backend.dashboard.tables import HistoryTable

from .models import Seminar
from .states import STATE_INFO


def render_pill(value, color="green"):
    # bg-red-200, bg-yellow-200, bg-green-200
    css_bg = " bg-{}-200".format(color)
    css_text = "text-{}-900".format(color)
    return format_html(
        '<span class="relative text-center inline-block px-3 py-1">'
        '<span class="absolute inset-0 rounded-full opacity-50 {}"></span>'
        '<span class="relative whitespace-no-wrap {}">{}</span>'
        "</span>",
        css_bg,
        css_text,
        value,
    )


class SeminarHistoryTable(HistoryTable):
    class Meta:
        exclude = ["history_object"]


class SeminarTable(tables.Table):
    title = tables.Column(linkify=True, attrs={"td": {"class": "primary-column"}})
    start_date = tables.DateColumn(
        verbose_name="Datum", format="d.m.y", attrs={"cell": {"class": "numeric"}}
    )
    owner = tables.Column(verbose_name="Besitzer_in", linkify=True)
    group = tables.Column(verbose_name="Gruppe", linkify=True)
    tnt = NumericColumn(verbose_name="TNT")
    funding = EuroColumn(verbose_name="Förderung")
    tnt_cost = EuroColumn(verbose_name="€/TNT")
    deadline = tables.DateColumn(
        verbose_name="Frist", format="d.m.y", attrs={"cell": {"class": "numeric"}}
    )

    def render_status(self, record, value):
        color = STATE_INFO[value]["color"]
        return render_pill(value, color)

    def render_deadline(self, record, value):
        status = record.deadline_status
        formatted = defaultfilters.date(value, "d.m.Y")
        if status == "not_applicable":
            return "—"
        if status == "not_soon":
            return formatted
        if status == "expired":
            color = "red"
        elif status == "soon":
            color = "yellow"
        return render_pill(formatted, color)

    class Meta:
        model = Seminar
        template_name = "table.html"
        fields = [
            "title",
            "start_date",
            "status",
            "owner",
            "group",
            "tnt",
            "funding",
            "tnt_cost",
            "deadline",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        attrs = {"class": "js-row-link table-sticky"}
        order_by = "-start_date"
        empty_text = "Keine Seminare gefunden."


class SeminarSearchTable(SeminarTable):

    year = tables.Column(verbose_name="Jahr")

    def render_year(self, record):
        return record.start_date.year

    class Meta:
        model = Seminar
        template_name = "table.html"
        fields = ["title", "year", "start_date", "status", "owner", "group"]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        attrs = {"class": "js-row-link table-sticky"}
        empty_text = "Keine Seminare gefunden."
