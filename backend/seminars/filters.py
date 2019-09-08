from django_filters import rest_framework as filters
from backend.seminars.models import Seminar
from backend.users.models import User
from backend.groups.models import JANUNGroup


class SeminarFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name="start_date__year")
    owner = filters.ModelChoiceFilter(
        queryset=User.objects.all(), to_field_name="username"
    )
    group = filters.ModelChoiceFilter(
        queryset=JANUNGroup.objects.all(), to_field_name="slug"
    )
    status = filters.ChoiceFilter(choices=Seminar.STATES)

    class Meta:
        model = Seminar
        fields = ["year", "owner", "group", "status"]
