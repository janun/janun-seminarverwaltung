from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter
from django.template import defaultfilters
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context

import django_tables2 as tables


def render_two_values(primary, secondary):
    return format_html(
        '<p class="whitespace-no-wrap">{}</p> '
        '<p class="whitespace-no-wrap text-xs text-gray-600 table-condensed-hidden">{}</p>',
        primary,
        secondary,
    )


def get_history_url(record):
    try:
        return record.instance.get_absolute_url()
    except ObjectDoesNotExist:
        return None


class HistoryTable(tables.Table):

    history_date = tables.Column(verbose_name="Wann", orderable=False)

    def render_history_date(self, record):
        value = record.history_date
        return render_two_values(
            NaturalTimeFormatter.string_for(value),
            defaultfilters.date(timezone.localtime(value), "d.m.Y H:i"),
        )

    history_user = tables.Column(verbose_name="Wer", orderable=False, linkify=True)

    def render_history_user(self, record):
        return record.history_user

    history_object = tables.Column(
        verbose_name="Was", orderable=False, linkify=get_history_url
    )

    def render_history_object(self, record):
        try:
            value = record.instance
        except ObjectDoesNotExist:
            value = record.history_object

        return defaultfilters.truncatechars(value, 70)

    changes = tables.Column(verbose_name="Änderungen", orderable=False, empty_values=())

    def render_changes(self, record):
        if record.history_type == "+":
            if record._meta.model_name == "historicalseminarcomment":
                return "Kommentar: {}".format(
                    defaultfilters.truncatechars(record.text, 150)
                )
            return format_html("<em>erstellt</em>")

        if record.history_type == "-":
            return format_html("<em>gelöscht</em>")

        if not record.changes:
            return format_html("<em>nichts geändert</em>")

        return Template(
            """<ul class="{% if changes|length > 1 %}list-disc{% endif %}">
        {% for change in changes %}
            <li class="mr-2 whitespace-no-wrap">
                <span>{{ change.field }}</span>:
                {% if not change.new %}
                    <em>gelöscht</em>
                {% elif not change.old %}
                    <span>{{ change.new|truncatechars:20 }}</span>
                {% else %}
                    <span class="line-through">{{ change.old|truncatechars:10 }}</span>
                    →
                    <span>{{ change.new|truncatechars:20 }}</span>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
        """
        ).render(Context({"changes": record.changes}))

    class Meta:
        template_name = "table.html"
        fields = ["history_date", "history_user", "history_object", "changes"]
        attrs = {"class": "table-sticky"}
