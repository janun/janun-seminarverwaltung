import re
import functools
from decimal import Decimal

from django.http import JsonResponse
from django.template.defaultfilters import floatformat
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from django import forms

from crispy_forms.layout import Fieldset as CrispyFieldset
from crispy_forms.layout import HTML
import django_tables2 as tables


class Fieldset(CrispyFieldset):
    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop("text", "")
        super().__init__(*args, **kwargs)


class Link(HTML):
    def __init__(self, href, text, css_class=""):
        html = '<a class="{2}" href="{0}">{1}</a>'.format(href, text, css_class)
        super().__init__(html)


def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count % 2 == 1:
        return values[int(round(count / 2))]
    return sum(values[count / 2 - 1 : count / 2 + 1]) / Decimal(2.0)


def format_number(value, decimals=0):
    if value is None:
        return None
    return re.sub(r"^(-?\d+)(\d{3})", r"\g<1>.\g<2>", floatformat(value, decimals))


def format_currency(value):
    return format_number(value, 2)


def format_with(formatter_func):
    """generic decorator, which formats return value with formatter_func"""

    def decorator(func_or_value):
        @functools.wraps(func_or_value)
        def wrapper(*args, **kwargs):
            return formatter_func(func_or_value(*args, **kwargs))

        if callable(func_or_value):
            return wrapper
        return formatter_func(func_or_value)

    return decorator


def slugify_german(content):
    return slugify(content.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe"))


def admin_change_url(obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse("admin:{}_{}_change".format(app_label, model_name), args=(obj.pk,))


def admin_link(func):
    @functools.wraps(func)
    def field_func(*args, **kwargs):
        related_obj = func(*args, **kwargs)
        if related_obj is None:
            return None
        url = admin_change_url(related_obj)
        return format_html('<a href="{}">{}</a>', url, str(related_obj))

    return field_func


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {"pk": self.object.pk}
            return JsonResponse(data)
        return response


class NumericColumn(tables.Column):
    attrs = {"cell": {"class": "numeric"}}


class EuroColumn(tables.TemplateColumn):
    template = "{{ value|default:0|default_if_none:'?'|floatformat:2 }} €"
    attrs = {"cell": {"class": "numeric"}}

    def __init__(self, *args, **kwargs):
        kwargs["template_code"] = self.template
        super().__init__(*args, **kwargs)


class ColoredBooleanColumn(tables.BooleanColumn):
    def render(self, value):
        if value:
            return format_html(
                '<div class="flex items-center justify-center h-5 w-5 rounded-full bg-green-200">'
                '<svg class="fill-current text-green-900 h-2 w-2" viewBox="0 0 20 20">'
                '<path d="M0 11l2-2 5 5L18 3l2 2L7 18z"/>'
                "</svg>"
                "</div>"
            )
        return format_html(
            '<div class="flex items-center justify-center h-5 w-5 rounded-full bg-red-200">'
            '<svg class="fill-current text-red-900 h-2 w-2" viewBox="0 0 20 20">'
            '<path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"/>'
            "</svg>"
            "</div>"
        )


class DateInput(forms.DateInput):
    template_name = "widgets/date_input.html"
