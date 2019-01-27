from django.db.models import Q
from django.forms import CheckboxSelectMultiple

import django_filters
# from django_filters.widgets import LinkWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, HTML

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
    role = django_filters.ChoiceFilter(
        choices=User.ROLES,
    )
    group = django_filters.ModelChoiceFilter(
        label="Gruppe", queryset=JANUNGroup.objects.all(), method=filter_group,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['name'].field.widget.attrs['autofocus'] = 'autofocus'
        self.form.helper = FormHelper()
        self.form.helper.form_tag = False
        self.form.helper.disable_csrf = True
        self.form.helper.layout = Layout(
            Div(
                Div('name', css_class='col-lg'),
                Div('role', css_class='col-lg'),
                Div('group', css_class='col-lg'),
                css_class='row'
            )
        )

    class Meta:
        model = User
        fields = ['name', ]
