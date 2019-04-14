import django_filters

from groups.models import JANUNGroup


class JANUNGroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Name", lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['name'].field.widget.attrs['autofocus'] = True
        self.filters['name'].field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = JANUNGroup
        fields = ['name', ]
