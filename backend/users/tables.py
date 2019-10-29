import django_tables2 as tables
from .models import User


class UserTable(tables.Table):
    name = tables.Column(linkify=True, attrs={"td": {"class": "primary-column"}})
    janun_groups = tables.ManyToManyColumn(
        verbose_name="Mitgliedschaften", linkify_item=True, default=""
    )
    group_hats = tables.ManyToManyColumn(
        verbose_name="Gruppen-Hüte", linkify_item=True, default=""
    )

    class Meta:
        model = User
        template_name = "table.html"
        fields = [
            "name",
            "username",
            "role",
            "janun_groups",
            "group_hats",
            "is_active",
            "is_reviewed",
            "last_visit",
        ]
        row_attrs = {"data-link": lambda record: record.get_absolute_url()}
        order_by = "name"
        empty_text = "Keine Konten gefunden."
