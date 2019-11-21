from itertools import chain
import re

from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q

from .tables import HistoryTable, SearchResultsTable
from .history import get_global_history
from backend.seminars.models import Seminar
from backend.groups.models import JANUNGroup
from backend.users.models import User


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
                get_global_history(5)[:5], attrs={"class": "table-condensed"}
            )
        return context


class GlobalHistoryView(UserPassesTestMixin, TemplateView):
    template_name = "dashboard/global_history.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = HistoryTable(get_global_history(100)[:100])
        return context


class SearchView(UserPassesTestMixin, TemplateView):
    context_object_name = "results"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def get_template_names(self):
        if self.request.is_ajax():
            return ["dashboard/ajax_search.html"]
        return ["dashboard/search.html"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        q = self.request.GET.get("q", None)
        results = self.get_results(q)
        context["count"] = self.count
        context["q"] = q
        context["results"] = results
        if not self.request.is_ajax():
            context["results_table"] = SearchResultsTable(results, orderable=False)
        return context

    def get_results(self, q):
        if re.match(r".*\d{4}$", q):
            year = q[-4:]
            rest = q[0:-4].strip()
            seminars = Seminar.objects.filter(
                Q(title__icontains=rest, start_date__year=year) | Q(title__icontains=q)
            ).only("title", "slug", "start_date")
        else:
            seminars = Seminar.objects.filter(title__icontains=q).only(
                "title", "slug", "start_date"
            )

        users = User.objects.filter(
            Q(name__icontains=q.strip()) | Q(username__icontains=q)
        )

        groups = JANUNGroup.objects.filter(name__icontains=q)

        self.count = seminars.count() + users.count() + groups.count()

        if self.request.is_ajax():
            seminars = seminars[:6]
            users = users[:6]
            groups = groups[:6]

        return chain(seminars, users, groups)

    def test_func(self):
        return self.request.user.is_staff
