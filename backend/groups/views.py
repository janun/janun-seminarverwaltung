from django.views.generic import (
    View,
    DetailView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy

from django_tables2.views import SingleTableMixin

from .models import JANUNGroup
from .tables import JANUNGroupTable
from .resources import JANUNGroupResource
from .forms import GroupCreateForm


class JANUNGroupUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = JANUNGroup
    success_message = "Änderung gespeichert."
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "group"
    form_class = GroupCreateForm
    template_name = "groups/group_update.html"

    def test_func(self):
        return self.request.user.is_superuser


class JANUNGroupDeleteView(SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = JANUNGroup
    success_url = reverse_lazy("groups:staff_list")
    success_message = "{} wurde gelöscht."
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "group"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message.format(name))
        return result


class JANUNGroupCreateView(UserPassesTestMixin, CreateView):
    form_class = GroupCreateForm
    template_name = "groups/group_create.html"

    def test_func(self):
        return self.request.user.is_superuser


class JANUNGroupStaffListView(SingleTableMixin, UserPassesTestMixin, ListView):
    model = JANUNGroup
    template_name = "groups/groups_staff.html"
    context_object_name = "group"
    table_class = JANUNGroupTable
    queryset = JANUNGroup.objects.add_annotations()

    def test_func(self):
        return self.request.user.is_staff


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
        context["seminars_next_year"] = (
            self.object.seminars.next_year()
            .annotate_funding()
            .annotate_tnt()
            .order_by("start_date")
        )
        context["stats_next_year"] = (
            context["seminars_next_year"].is_not_rejected().get_aggregates()
        )
        context["seminars_this_year"] = (
            self.object.seminars.this_year()
            .annotate_funding()
            .annotate_tnt()
            .order_by("start_date")
        )
        context["stats_this_year"] = (
            context["seminars_this_year"].is_not_rejected().get_aggregates()
        )
        context["seminars_last_year"] = (
            self.object.seminars.last_year()
            .annotate_funding()
            .annotate_tnt()
            .order_by("start_date")
        )
        context["stats_last_year"] = (
            context["seminars_last_year"].is_not_rejected().get_aggregates()
        )
        return context


class JANUNGroupExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        qs = JANUNGroup.objects.all()
        dataset = JANUNGroupResource().export(qs)
        filename = "janun_groups.csv"
        response = HttpResponse(dataset.csv, content_type="csv")
        response["Content-Disposition"] = "attachment; filename={}".format(filename)
        return response
