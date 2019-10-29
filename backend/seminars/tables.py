import django_tables2 as tables
from django.utils.html import format_html

from .models import Seminar


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
    training_days = tables.Column(
        verbose_name="B-Tage", attrs={"cell": {"class": "numeric"}}
    )
    attendees = tables.Column(verbose_name="TN", attrs={"cell": {"class": "numeric"}})
    tnt = tables.Column(verbose_name="TNT", attrs={"cell": {"class": "numeric"}})
    funding = tables.TemplateColumn(
        """{{ record.funding|default:0|default_if_none:'?'|floatformat:2 }} €""",
        verbose_name="Förderung",
        attrs={"cell": {"class": "numeric"}},
    )
    tnt_cost = tables.TemplateColumn(
        """{{ record.tnt_cost|default:0|default_if_none:'?'|floatformat:2 }} €""",
        verbose_name="€/TNT",
        attrs={"cell": {"class": "numeric"}},
    )
    deadline = tables.DateColumn(
        verbose_name="Deadline", format="d.m.y", attrs={"cell": {"class": "numeric"}}
    )
    created_at = tables.DateColumn(
        verbose_name="angemeldet", format="d.m.y", attrs={"cell": {"class": "numeric"}}
    )

    def render_deadline(self, record):
        status = record.deadline_status
        deadline = record.deadline.strftime("%d.%m.%y")
        if status == "not_applicable":
            return "n.z."
        if status == "not_soon":
            return deadline
        if status == "expired":
            css_class = "bg-red-500"
        elif status == "soon":
            css_class = "bg-yellow-500"
        return format_html(
            '<span class="inline-block h-2 w-2 mr-1 rounded-full {}"></span> {}',
            css_class,
            deadline,
        )

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
            "training_days",
            "attendees",
            "tnt",
            "funding",
            "tnt_cost",
            "deadline",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        order_by = "-start_date"
        empty_text = "Keine Seminare gefunden."
