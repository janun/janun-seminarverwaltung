from django_filters import rest_framework as filters
from . import models


class SeminarFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name="start_date__year")
    owner = filters.ModelChoiceFilter(
        queryset=models.User.objects.all(), to_field_name="username"
    )
    group = filters.ModelChoiceFilter(
        queryset=models.JANUNGroup.objects.all(), to_field_name="slug"
    )
    status = filters.ChoiceFilter(choices=models.Seminar.STATES)

    class Meta:
        model = models.Seminar
        fields = ["year", "owner", "group", "status"]


class UserFilter(filters.FilterSet):
    is_reviewed = filters.BooleanFilter()

    class Meta:
        model = models.User
        fields = ["is_reviewed"]
