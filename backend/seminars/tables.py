import django_tables2 as tables
from django.utils.html import format_html

from backend.utils import NumericColumn, EuroColumn

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


class SeminarTable(tables.Table):
    # checkbox = tables.CheckBoxColumn(
    #     accessor="pk", attrs={"input": {"class": "form-checkbox"}}
    # )
    title = tables.Column(linkify=True, attrs={"td": {"class": "primary-column"}})
    start_date = tables.DateColumn(
        verbose_name="Datum", format="d.m.y", attrs={"cell": {"class": "numeric"}}
    )
    owner = tables.Column(verbose_name="Besitzer_in", linkify=True)
    group = tables.Column(verbose_name="Gruppe", linkify=True)
    # training_days = tables.Column(
    #     verbose_name="B-Tage", attrs={"cell": {"class": "numeric"}}
    # )
    # attendees = tables.Column(verbose_name="TN", attrs={"cell": {"class": "numeric"}})
    tnt = NumericColumn(verbose_name="TNT")
    funding = EuroColumn(verbose_name="Förderung")
    tnt_cost = EuroColumn(verbose_name="€/TNT")
    deadline = tables.DateColumn(
        verbose_name="Deadline", format="d.m.y", attrs={"cell": {"class": "numeric"}}
    )
    created_at = tables.DateColumn(
        verbose_name="angemeldet", format="d.m.y", attrs={"cell": {"class": "numeric"}}
    )

    def render_status(self, record, value):
        color = STATE_INFO[value]["color"]
        return render_pill(value, color)

    def render_deadline(self, record):
        status = record.deadline_status
        deadline = record.deadline.strftime("%d.%m.%y")
        if status == "not_applicable":
            return "—"
        if status == "not_soon":
            return deadline
        if status == "expired":
            color = "red"
        elif status == "soon":
            color = "yellow"
        return render_pill(deadline, color)

    class Meta:
        model = Seminar
        template_name = "table.html"
        fields = [
            # "checkbox",
            "title",
            "start_date",
            "status",
            "owner",
            "group",
            # "training_days",
            # "attendees",
            "tnt",
            "funding",
            "tnt_cost",
            "deadline",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        attrs = {"class": "js-data-link"}
        order_by = "-start_date"
        empty_text = "Keine Seminare gefunden."
