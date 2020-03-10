from django import forms
from django.db.models import Q

import django_filters

from backend.emails.models import EmailTemplate


class SearchInput(forms.TextInput):
    template_name = "widgets/search_input.html"


class EmailTemplateFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        label="Suche",
        widget=SearchInput(attrs={"autofocus": True}),
        method="filter_search",
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(description__icontains=value))

    class Meta:
        model = EmailTemplate
        fields = ["search"]
