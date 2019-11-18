from django import forms
from django.db.models import Q

import django_filters

from backend.users.models import User
from backend.groups.models import JANUNGroup


class SearchInput(forms.TextInput):
    template_name = "widgets/search_input.html"


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Filter nach Name",
        widget=SearchInput(attrs={"autofocus": True}),
        method="filter_name",
    )
    role = django_filters.ChoiceFilter(label="Rolle", choices=User.ROLES)
    janun_groups = django_filters.ModelChoiceFilter(
        label="Mitgliedschaft",
        null_label="keine",
        queryset=JANUNGroup.objects.order_by("name").all(),
    )
    group_hats = django_filters.ModelChoiceFilter(
        label="Gruppen-Hut",
        null_label="keine",
        queryset=JANUNGroup.objects.order_by("name").all(),
    )

    is_reviewed = django_filters.ChoiceFilter(
        choices=((True, "überprüft"), (False, "nicht überprüft"))
    )

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(username__icontains=value))

    class Meta:
        model = User
        fields = ["name", "role", "janun_groups", "group_hats", "is_reviewed"]
