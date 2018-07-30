from django import template
from django.utils.html import format_html_join


register = template.Library()


@register.filter()
def link_list(object_list):
    """returns comma seperated list of links to object"""
    return format_html_join(
        ", ",
        '<a href="{}">{}</a>',
        ((object.get_absolute_url(), object) for object in object_list)
    )
