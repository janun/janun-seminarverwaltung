from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter
from django.template import defaultfilters
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context

import django_tables2 as tables


def render_two_values(primary, secondary):
    return format_html(
        '<p class="whitespace-no-wrap">{}</p>'
        '<p class="whitespace-no-wrap text-xs text-gray-600">{}</p>',
        primary,
        secondary,
    )


def get_history_changes(entry):
    changes = []
    for change in entry.diff_against(entry.prev_record).changes:
        field = entry.instance._meta.get_field(change.field).verbose_name
        if change.field == "password":
            changes.append({"field": field, "old": "", "new": "geändert"})
        else:
            changes.append({"field": field, "old": change.old, "new": change.new})
    return changes


def get_history_url(record):
    try:
        return record.instance.get_absolute_url()
    except ObjectDoesNotExist:
        return ""


class HistoryTable(tables.Table):

    history_date = tables.Column(
        verbose_name="Zeitpunkt", orderable=False, attrs={"cell": {"class": "numeric"}}
    )

    def render_history_date(self, record):
        value = record.history_date
        return render_two_values(
            NaturalTimeFormatter.string_for(value),
            defaultfilters.date(timezone.localtime(value), "d.m.Y H:i"),
        )

    history_user = tables.Column(
        verbose_name="Konto / Rolle", orderable=False, linkify=True
    )

    def render_history_user(self, record):
        value = record.history_user
        return render_two_values(value, value.role)

    history_object = tables.Column(
        verbose_name="Objekt / Objekttyp", orderable=False, linkify=get_history_url
    )

    def render_history_object(self, record):
        try:
            value = record.instance
        except ObjectDoesNotExist:
            value = record.history_object
        return render_two_values(
            defaultfilters.truncatechars(value, 70), value._meta.verbose_name.title()
        )

    changes = tables.Column(verbose_name="Details", orderable=False, empty_values=())

    def render_changes(self, record):
        if record.history_type == "+":
            if record._meta.model_name == "historicalseminarcomment":
                return "Kommentar: {}".format(
                    defaultfilters.truncatechars(record.text, 150)
                )
            return "hinzugefügt"

        if record.history_type == "-":
            return "gelöscht"

        changes = get_history_changes(record)
        return Template(
            """
        {% for change in changes %}
            <span class="mr-2 whitespace-no-wrap">
                <span class="text-gray-600 text-xs">{{ change.field }}</span>:
                {% if not change.new %}
                    <span class="line-through">{{ change.old|truncatechars:20 }}</span>
                {% elif not change.old %}
                    <span>{{ change.new|truncatechars:20 }}</span>
                {% else %}
                    <span class="line-through">{{ change.old|truncatechars:10 }}</span>
                    <span>{{ change.new|truncatechars:20 }}</span>
                {% endif %}
            </span>
        {% endfor %}
        """
        ).render(Context({"changes": changes}))

    class Meta:
        template_name = "table.html"
        fields = ["history_date", "history_user", "history_object", "changes"]
        attrs = {"class": "table-hover table-sticky"}
