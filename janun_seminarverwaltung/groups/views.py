from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect

from rules.contrib.views import PermissionRequiredMixin
from braces.views import PrefetchRelatedMixin
from django_tables2 import SingleTableView

from seminars.models import Seminar

from groups.models import JANUNGroup, ContactPerson
from .tables import JANUNGroupTable
from .forms import JANUNGroupForm, ContactPeopleInlineFormSet


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
    prefetch_related = ['members', 'contact_people']
    permission_required = 'groups.detail_janungroup'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seminars'] = Seminar.objects.filter(group=self.object)[:6]
        context['contact_people'] = self.get_object().contact_people.all()
        return context


class JANUNGroupCreateView(PermissionRequiredMixin, CreateView):
    model = JANUNGroup
    form_class = JANUNGroupForm
    permission_required = 'groups.add_janungroup'
    raise_exception = True
    template_name_suffix = '_create'

    # https://github.com/dfunckt/django-rules/issues/85
    def get_object(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['contact_people_form'] = ContactPeopleInlineFormSet(self.request.POST)
        else:
            context['contact_people_form'] = ContactPeopleInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        contact_people_form = context['contact_people_form']
        if contact_people_form.is_valid():
            self.object = form.save()
            contact_people_form.instance = self.object
            contact_people_form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))


class JANUNGroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = JANUNGroup
    success_url = reverse_lazy('groups:list')
    permission_required = 'groups.delete_janungroup'
    raise_exception = True


class JANUNGroupUpdateView(PermissionRequiredMixin, UpdateView):
    model = JANUNGroup
    form_class = JANUNGroupForm
    permission_required = 'groups.edit_janungroup'
    raise_exception = True
    template_name_suffix = '_edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['contact_people_form'] = ContactPeopleInlineFormSet(self.request.POST, instance=self.object)
        else:
            context['contact_people_form'] = ContactPeopleInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        contact_people_form = context['contact_people_form']
        if contact_people_form.is_valid():
            self.object = form.save()
            contact_people_form.instance = self.object
            contact_people_form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))
