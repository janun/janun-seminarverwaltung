import re
from django import template
from django import forms
from django.utils.html import conditional_escape, mark_safe

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


@register.filter(needs_autoescape=True)
def highlight(text, sterm, autoescape=None):
    text = str(text)
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    pattern = re.compile("(%s)" % esc(sterm), re.IGNORECASE)
    result = pattern.sub(r"<strong>\1</strong>", text)
    return mark_safe(result)
