import datetime

from django import forms

import django_filters

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML

from seminars.models import Seminar
from groups.models import JANUNGroup
from janun_seminarverwaltung.users.models import User


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


class SeminarTeamerFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label="Suche", lookup_expr='icontains')
    # start_year = YearFilter(label="Jahr", field_name="start_date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title'].field.widget.attrs['autofocus'] = True
        self.filters['title'].field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Seminar
        fields = ['title']


class SeminarStaffFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label="Titel", lookup_expr='icontains')
    start_year = YearFilter(label="Jahr", field_name="start_date")
    start_quarter = django_filters.ChoiceFilter(
        label="Quartal", field_name="start_date", lookup_expr='quarter',
        choices=[(i, "{0}".format(i)) for i in range(1, 5)]
    )
    state = django_filters.ChoiceFilter(
        choices=Seminar.STATUS
    )
    group = django_filters.ModelChoiceFilter(
        null_label='keine', queryset=JANUNGroup.objects.order_by('name').all()
    )
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.order_by('name').all()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title'].field.widget.attrs['autofocus'] = True
        self.filters['title'].field.widget.attrs['autocomplete'] = 'off'
        self.form.helper = FormHelper()
        self.form.helper.form_tag = False
        self.form.helper.disable_csrf = True

    class Meta:
        model = Seminar
        fields = ['title', 'start_year', 'start_quarter', 'state', 'group', 'author']
