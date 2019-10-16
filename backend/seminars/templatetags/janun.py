from django import template
from django import forms

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
