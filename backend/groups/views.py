from django.views.generic import DetailView, ListView, CreateView
from django.db.models import Sum
from django.contrib.auth.mixins import UserPassesTestMixin

from django_tables2.views import SingleTableMixin

from .models import JANUNGroup
from .tables import JANUNGroupTable


class JANUNGroupAddView(CreateView):
    model = JANUNGroup


class JANUNGroupStaffListView(SingleTableMixin, UserPassesTestMixin, ListView):
    model = JANUNGroup
    template_name = "groups/groups_staff.html"
    context_object_name = "group"
    table_class = JANUNGroupTable

    def test_func(self):
        if self.request.user.is_staff:
            return True


class JANUNGroupDetailView(UserPassesTestMixin, DetailView):
    model = JANUNGroup
    template_name = "groups/group_detail.html"
    context_object_name = "group"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        if not self.request.user.is_reviewed:
            return False
        return (
            self.get_object() in self.request.user.janun_groups.all()
            or self.get_object() in self.request.user.group_hats.all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seminars_next_year"] = self.object.seminars.next_year().order_by(
            "start_date"
        )
        context["stats_next_year"] = (
            context["seminars_next_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        context["seminars_this_year"] = self.object.seminars.this_year().order_by(
            "start_date"
        )
        context["stats_this_year"] = (
            context["seminars_this_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        context["seminars_last_year"] = self.object.seminars.last_year().order_by(
            "start_date"
        )
        context["stats_last_year"] = (
            context["seminars_last_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        return context
