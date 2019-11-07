from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin

from simple_history.models import registered_models
from operator import attrgetter

from .tables import HistoryTable


def get_global_history(self, length=10):
    history = []
    for model in registered_models.values():
        for entry in model.history.all()[:length]:
            history.append(entry)
    return sorted(history, key=attrgetter("history_date"), reverse=True)


class Dashboard(TemplateView):
    template_name = "dashboard/dashboard.html"
    seminar_limit = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["janun_groups"] = self.request.user.janun_groups.all()
        context["group_hats"] = self.request.user.group_hats.all()
        context["seminars"] = self.request.user.seminars.all().order_by("created_at")[
            : self.seminar_limit
        ]
        context["show_more_link"] = (
            self.request.user.seminars.count() > self.seminar_limit
        )
        if self.request.user.is_staff:
            context["history_table"] = HistoryTable(
                get_global_history(5)[:5],
                attrs={"class": "table-condensed"},
                show_header=False,
            )
        return context


class GlobalHistoryView(UserPassesTestMixin, TemplateView):
    template_name = "dashboard/global_history.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = HistoryTable(get_global_history(50))
        return context
