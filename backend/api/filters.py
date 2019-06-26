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

    class Meta:
        model = models.Seminar
        fields = ["year", "owner", "group"]
