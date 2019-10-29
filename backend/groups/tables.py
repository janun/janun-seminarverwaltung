import django_tables2 as tables
from django.utils.html import format_html
from django.utils import timezone

from .models import JANUNGroup


class NumericColumn(tables.Column):
    attrs = {"cell": {"class": "numeric"}}


class EuroColumn(tables.TemplateColumn):
    template = "{{ record.tnt_cost_simple_this_year|default:0|default_if_none:'?'|floatformat:2 }} €"
    attrs = {"cell": {"class": "numeric"}}

    def __init__(self, *args, **kwargs):
        kwargs["template_code"] = self.template
        super().__init__(*args, **kwargs)


class JANUNGroupTable(tables.Table):
    name = tables.Column(linkify=True, attrs={"td": {"class": "primary-column"}})
    members = tables.ManyToManyColumn(
        verbose_name="Mitglieder", linkify_item=True, default=""
    )
    group_hats = tables.ManyToManyColumn(
        verbose_name="Hüte", linkify_item=True, default=""
    )
    seminars_this_year = NumericColumn(
        verbose_name="Seminare {}".format(timezone.now().year)
    )
    funding_this_year = EuroColumn(verbose_name="Förderung")
    tnt_this_year = NumericColumn(verbose_name="TNT")
    tnt_cost_simple_this_year = EuroColumn(verbose_name="€/TNT")

    class Meta:
        model = JANUNGroup
        template_name = "table.html"
        fields = [
            "name",
            "members",
            "group_hats",
            "seminars_this_year",
            "funding_this_year",
            "tnt_this_year",
            "tnt_cost_simple_this_year",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        order_by = "name"
        empty_text = "Keine Gruppen gefunden."
