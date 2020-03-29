from django.utils import timezone

import django_tables2 as tables

from backend.utils import NumericColumn, EuroColumn

from .models import JANUNGroup


class JANUNGroupTable(tables.Table):
    name = tables.Column(linkify=True, attrs={"td": {"class": "primary-column"}})
    members = tables.ManyToManyColumn(
        verbose_name="Mitglieder", linkify_item=True, default=""
    )
    group_hats = tables.ManyToManyColumn(
        verbose_name="Gruppenhut", linkify_item=True, default=""
    )
    seminars_this_year = NumericColumn(
        verbose_name="Seminare {}".format(timezone.now().year)
    )
    funding_this_year = EuroColumn(verbose_name="Förderung")
    tnt_this_year = NumericColumn(verbose_name="TNT (JFG)")
    tnt_cost_simple_this_year = EuroColumn(verbose_name="€/TNT (JFG)")

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
        attrs = {"class": "js-row-link table-sticky"}
        order_by = "name"
        empty_text = "Keine Gruppen gefunden."
