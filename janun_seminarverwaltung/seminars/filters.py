import django_filters

from seminars.models import Seminar
from groups.models import JANUNGroup


class YearFilter(django_filters.ChoiceFilter):

    def __init__(self, *args, **kwargs):
        kwargs['lookup_expr'] = "year"
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        qs = self.model._default_manager.distinct()
        qs = qs.order_by(self.field_name).dates(self.field_name, 'year')
        self.extra['choices'] = [(o.year, o.year) for o in qs]
        return super().field


class QuarterFilter(django_filters.ChoiceFilter):

    def __init__(self, *args, **kwargs):
        kwargs['lookup_expr'] = "month__in"
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        self.extra['choices'] = [
            (i, "{0}. Quartal".format(i)) for i in range(1, 5)
        ]
        return super().field

    def filter(self, qs, value):
        if value:
            v = int(value)*3
            value = (v-2, v-1, v)
        return super().filter(qs, value)


class AllValuesModelFilter(django_filters.AllValuesFilter):
    pass


class SeminarFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label="Titel", lookup_expr='icontains')
    start_year = YearFilter(label="Jahr", name="start")
    start_quarter = QuarterFilter(label="Quartal", name="start")
    group = django_filters.ModelChoiceFilter(
        name='group',
        null_label='-- keine --',
        queryset=JANUNGroup.objects.all(),
    )
    # author = AllValuesModelFilter()

    class Meta:
        model = Seminar
        fields = ['title', 'group', 'state', 'author', 'start_year', 'start_quarter']
