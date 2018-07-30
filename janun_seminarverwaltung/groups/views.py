from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy

from rules.contrib.views import PermissionRequiredMixin
from braces.views import PrefetchRelatedMixin
from django_tables2 import SingleTableView

from groups.models import JANUNGroup
from seminars.models import Seminar
from .tables import JANUNGroupTable


class JANUNGroupListView(SingleTableView):
    model = JANUNGroup
    table_class = JANUNGroupTable

    def get_queryset(self):
        if self.request.user.role == "TEAMER":
            return self.request.user.janun_groups.all()
        if self.request.user.role == "PRUEFER":
            return self.request.user.group_hats.all()
        if self.request.user.role == "VERWALTER":
            return JANUNGroup.objects.all()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == "VERWALTER":
            context['heading'] = "Alle Gruppen ({0})".format(len(self.object_list))
        else:
            context['heading'] = "Deine Gruppen ({0})".format(len(self.object_list))
        return context


class JANUNGroupDetailView(PermissionRequiredMixin, DetailView, PrefetchRelatedMixin):
    model = JANUNGroup
    prefetch_related = ['members']
    permission_required = 'groups.detail_janungroup'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seminars'] = Seminar.objects.filter(group=self.object)
        return context


class JANUNGroupCreateView(PermissionRequiredMixin, CreateView):
    model = JANUNGroup
    fields = ['name', 'logo']
    permission_required = 'groups.add_janungroup'
    raise_exception = True


class JANUNGroupDeleteView(DeleteView):
    model = JANUNGroup
    success_url = reverse_lazy('groups:list')
    permission_required = 'groups.delete_janungroup'
    raise_exception = True

# TODO: UpdateView
