from django import template
from django import forms

import django_filters

from backend.utils import format_number

register = template.Library()


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
