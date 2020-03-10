import re
from django import template
from django import forms
from django.utils.html import conditional_escape, mark_safe
from django.contrib.sites.shortcuts import get_current_site

import django_filters

from backend.utils import format_number
from backend.users.models import User
from backend.seminars.models import Seminar

register = template.Library()


@register.simple_tag()
def get_unreviewed_users() -> int:
    """Get number of users with is_reviewed=False"""
    return User.objects.filter(is_reviewed=False).count()


@register.simple_tag()
def get_new_seminars() -> int:
    """Get number of seminars with status angemeldet"""
    return Seminar.objects.filter(status="angemeldet").count()


@register.filter
def number(value, decimals=2) -> str:
    """format number, defaulting to currencies"""
    return format_number(value, decimals)


@register.filter
def is_selectmultiple(field) -> bool:
    """helper for crispy forms"""
    return isinstance(field.field.widget, forms.SelectMultiple)


@register.filter
def is_textarea(field) -> bool:
    """helper for crispy forms"""
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def is_linkwidget(field) -> bool:
    """helper for crispy forms"""
    return isinstance(field.field.widget, django_filters.widgets.LinkWidget)


@register.filter
def get_modelname(instance) -> str:
    """get verbose name of model from instance"""
    return instance._meta.verbose_name


@register.filter(needs_autoescape=True)
def highlight(text: str, search_term: str, autoescape=False) -> str:
    """helper for search results to highlight the search term in text using strong"""
    text = str(text)
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    pattern = re.compile("(%s)" % esc(search_term), re.IGNORECASE)
    result = pattern.sub(r"<strong>\1</strong>", text)
    return mark_safe(result)


@register.simple_tag(takes_context=True)
def absurl(context, location: str) -> str:
    """return the absolute uri, i.e. containing scheme and host from location"""
    try:
        request = context["request"]
        return request.build_absolute_uri(location)
    except KeyError:
        domain = get_current_site(None).domain
        return "https://" + domain + location
