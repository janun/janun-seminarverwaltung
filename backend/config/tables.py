import django_tables2 as tables

from backend.seminars.models import FundingRate


class FundingRateTable(tables.Table):
    year = tables.Column(linkify=True, attrs={"td": {"class": "primary-column"}})

    class Meta:
        model = FundingRate
        template_name = "table.html"
        fields = ["year", "group_rate", "single_rate"]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        attrs = {"class": "js-row-link table-sticky"}
        order_by = "-year"
        empty_text = "Keine Förderungen gefunden."
