import datetime

from django import forms

import django_filters

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML

from seminars.models import Seminar
from groups.models import JANUNGroup
from janun_seminarverwaltung.users.models import User


class YearFilter(django_filters.NumberFilter):
    def __init__(self, *args, **kwargs):
        kwargs['lookup_expr'] = "year"
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        qs = self.model._default_manager.distinct().order_by(self.field_name)
        self.extra['min_value'] = qs.first().start_date.year
        self.extra['max_value'] = qs.last().start_date.year
        return super().field


def allowed_groups(request):
    if request is None:
        return JANUNGroup.objects.none()
    user = request.user
    if user.role == 'VERWALTER':
        return JANUNGroup.objects.all()
    if user.role == 'PRUEFER':
        return user.group_hats.all()
    return user.janun_groups.all()


def allowed_users(request):
    if request is None:
        return User.objects.none()
    user = request.user
    if user.role in ('VERWALTER', 'PRUEFER'):
        return User.objects.all()
    return User.objects.filter(pk=user.pk)


def filter_timing(qs, field, value):
    if value == 'past':
        return qs.filter(end_date__lt=datetime.date.today())
    if value == 'future':
        return qs.filter(start_date__gte=datetime.date.today())
    if value == 'running':
        return qs.filter(start_date=datetime.date.today())
    return qs


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
    start_quarter = django_filters.NumberFilter(
        label="Quartal", field_name='start_date', lookup_expr='quarter',
        min_value=1, max_value=4
    )
    # start_quarter = django_filters.ChoiceFilter(
    #     label="Quartal", field_name="start_date", lookup_expr='quarter',
    #     choices=[(i, "{0}".format(i)) for i in range(1, 5)]
    # )
    state = django_filters.ChoiceFilter(
        choices=Seminar.STATUS
    )
    group = django_filters.ModelChoiceFilter(
        null_label='keine', queryset=allowed_groups,
    )
    author = django_filters.ModelChoiceFilter(
        queryset=allowed_users
    )
    # timing = django_filters.ChoiceFilter(
    #     label="Zeitpunkt", field_name="start_date",
    #     choices=[('past', "Vergangenheit"), ('running', 'Läuft'), ('future', "Zukunft")],
    #     method=filter_timing
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title'].field.widget.attrs['autofocus'] = True
        self.filters['title'].field.widget.attrs['autocomplete'] = 'off'
        self.form.helper = FormHelper()
        self.form.helper.form_tag = False
        self.form.helper.disable_csrf = True
        self.form.helper.layout = Layout(
            'title',
            Div(
                Div('start_year', css_class='col-6 pr-1'),
                Div('start_quarter', css_class='col-6 pl-1'),
                css_class='row d-inline-flex'
            ),
            Field('state', css_class='js-select-dis'),
            Field('group', css_class='js-select-dis'),
            Field('author', css_class='js-select-dis'),
        )

    class Meta:
        model = Seminar
        fields = ['title', 'start_year', 'start_quarter', 'state', 'group', 'author']
