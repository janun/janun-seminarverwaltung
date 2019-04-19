import django_filters

from . import models


class YearFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs['lookup_expr'] = "year"
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        qs = self.model._default_manager.distinct().order_by(self.field_name)
        qs = qs.order_by(self.field_name).dates(self.field_name, 'year', order='DESC')
        self.extra['choices'] = [(o.year, o.year) for o in qs]
        return super().field


class SeminarFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    start_year = YearFilter(field_name="start_date")
    start_quarter = django_filters.ChoiceFilter(
        field_name="start_date", lookup_expr='quarter',
        choices=[(i, "{0}".format(i)) for i in range(1, 5)]
    )

    class Meta:
        model = models.Seminar
        fields = ['title', 'start_year', 'start_quarter', 'status', 'group', 'owner']
