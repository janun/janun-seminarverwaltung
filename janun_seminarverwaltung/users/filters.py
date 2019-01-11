from django.db.models import Q

import django_filters

from groups.models import JANUNGroup
from janun_seminarverwaltung.users.models import User

def filter_group(qs, field, value):
    return qs.filter(
        Q(janun_groups=value)
        | Q(group_hats=value)
    )

def search(qs, field, value):
    return qs.filter(
        Q(name__icontains=value)
        | Q(email__icontains=value)
        | Q(username__icontains=value)
    )

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Suche", method=search)
    role = django_filters.ChoiceFilter(choices=User.ROLES)
    group = django_filters.ModelChoiceFilter(
        label="Gruppe", queryset=JANUNGroup.objects.all(), method=filter_group,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['name'].field.widget.attrs['autofocus'] = 'autofocus'

    class Meta:
        model = User
        fields = ['name', ]
