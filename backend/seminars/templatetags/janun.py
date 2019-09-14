from django import template

from backend.utils import format_number

register = template.Library()


@register.filter
def number(value, decimals=2):
    return format_number(value, decimals)
