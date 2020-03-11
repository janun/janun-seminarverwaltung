from itertools import chain
import re

from django.views.generic import TemplateView, ListView
from django.db.models import Q, Max

from backend.seminars.models import Seminar
from backend.groups.models import JANUNGroup
from backend.users.models import User
from backend.mixins import StaffOnlyMixin
from .tables import HistoryTable, SearchResultsTable
from .history import get_global_history


class Dashboard(TemplateView):
    template_name = "dashboard/dashboard.html"
    seminar_limit = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["janun_groups"] = self.request.user.janun_groups.all()
        context["group_hats"] = self.request.user.group_hats.all()
        context["seminars"] = (
            self.request.user.seminars.annotate_tnt()
            .all()
            .annotate_funding()
            .annotate_deadline_status()
            .select_related("owner", "group")
            .order_by("created_at")[: self.seminar_limit]
        )
        context["show_more_link"] = (
            self.request.user.seminars.count() > self.seminar_limit
        )
        if self.request.user.is_staff:
            context["history_table"] = HistoryTable(
                get_global_history(50, after_limit=5),
                attrs={"class": "table-condensed"},
            )
        return context


class GlobalHistoryView(StaffOnlyMixin, TemplateView):
    template_name = "dashboard/global_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = int(self.request.GET.get("page", "1"))
        context["page"] = page
        context["table"] = HistoryTable(
            get_global_history(limit=100, offset=(page - 1) * 100)
        )
        return context


class SearchView(StaffOnlyMixin, TemplateView):
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
            context["results_table"] = SearchResultsTable(results, orderable=False, q=q)
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
        ).only("name", "username")

        groups = JANUNGroup.objects.filter(name__icontains=q).only("name")

        self.count = seminars.count() + users.count() + groups.count()

        if self.request.is_ajax():
            seminars = seminars[:6]
            users = users[:6]
            groups = groups[:6]

        return chain(users, groups, seminars)


class LastViewedSeminarsView(StaffOnlyMixin, ListView):
    template_name = "dashboard/last_viewed_seminars.html"
    context_object_name = "seminars"

    def get_queryset(self):
        qs = (
            Seminar.objects.all()
            .annotate(view_time=Max("views__when"))
            .order_by("-view_time")
            .filter(view_time__isnull=False, views__user=self.request.user)
        )
        return qs[:6]
