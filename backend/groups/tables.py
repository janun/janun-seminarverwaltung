import django_tables2 as tables
from django.utils.html import format_html
from django.utils import timezone

from backend.utils import NumericColumn, EuroColumn

from .models import JANUNGroup


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
