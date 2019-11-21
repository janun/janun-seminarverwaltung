from django import template
from django import forms

import django_filters

from backend.utils import format_number
from backend.users.models import User
from backend.seminars.models import Seminar

register = template.Library()


@register.simple_tag()
def get_unreviewed_users():
    return User.objects.filter(is_reviewed=False).count()


@register.simple_tag()
def get_new_seminars():
    return Seminar.objects.filter(status="angemeldet").count()


@register.filter
def number(value, decimals=2):
    return format_number(value, decimals)


@register.filter
def is_selectmultiple(field):
    return isinstance(field.field.widget, forms.SelectMultiple)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_linkwidget(field):
    return isinstance(field.field.widget, django_filters.widgets.LinkWidget)


@register.filter
def get_modelname(instance):
    return instance._meta.verbose_name
