from collections import OrderedDict

from django.views.generic import DetailView, DeleteView, ListView
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
# from django.core.exceptions import PermissionDenied

from rules.contrib.views import PermissionRequiredMixin
from braces.views import SelectRelatedMixin
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from formtools.wizard.views import NamedUrlSessionWizardView

from seminars.models import Seminar
from seminars.tables import SeminarTable
from seminars.filters import SeminarFilter
import seminars.forms as seminar_forms


class SeminarListView(FilterView, SingleTableView):
    model = Seminar
    table_class = SeminarTable
    filterset_class = SeminarFilter
    template_name = "seminars/seminar_list.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orig_count = 0  # count before filter

    def get_queryset(self):
        # everyone sees their own seminars
        qs = Seminar.objects.filter(author=self.request.user)
        # pruefer also sees seminars for their groups
        if self.request.user.role == "PRUEFER":
            qs |= Seminar.objects.filter(group__in=self.request.user.group_hats.all())
        # verwalter simply can see all seminars
        if self.request.user.role == "VERWALTER":
            qs = Seminar.objects.all()
        qs = qs.select_related('group', 'author')
        self.orig_count = qs.count()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heading = "Deine Seminare"
        if self.request.user.role == "PRUEFER":
            heading = "Seminare Deiner Gruppen"
        if self.request.user.role == "VERWALTER":
            heading = "Alle Seminare"

        count = len(self.object_list)
        if count != self.orig_count:
            heading = heading + " (%s/%s)" % (count, self.orig_count)
        else:
            heading = heading + " (%s)" % count

        context['heading'] = heading
        context['orig_count'] = self.orig_count
        return context


class SeminarDetailView(PermissionRequiredMixin, SelectRelatedMixin, DetailView):
    model = Seminar
    select_related = ['author', 'group']
    permission_required = 'seminars.detail_seminar'
    raise_exception = True


# class SeminarCreateView(PermissionRequiredMixin, CreateView):
#     model = Seminar
#     fields = ['title', 'start', 'end', 'group', 'author', 'state']
#     permission_required = 'seminars.add_seminar'
#     raise_exception = True
#
#     def get_initial(self):
#         initial = super().get_initial()
#         initial['author'] = self.request.user
#         initial['group'] = self.request.user.janun_groups.first()
#         return initial


class SeminarWizardView(PermissionRequiredMixin, NamedUrlSessionWizardView):
    permission_required = 'seminars.add_seminar'
    raise_exception = True
    template_name = "seminars/seminar_wizard.html"
    form_list = (
        ('content', seminar_forms.ContentSeminarForm),
        ('datetime', seminar_forms.DatetimeSeminarForm),
        ('location', seminar_forms.LocationSeminarForm),
        ('group', seminar_forms.GroupSeminarForm),
        ('days', seminar_forms.TrainingDaysSeminarForm),
        ('attendees', seminar_forms.AttendeesSeminarForm),
        ('funding', seminar_forms.FundingSeminarForm),
        ('barriers', seminar_forms.BarrierSeminarForm),
        ('confirm', seminar_forms.ConfirmSeminarForm),
    )

    def get_template_names(self):
        return [
            'seminars/seminar_wizard_%s.html' % self.steps.current,
            self.template_name
        ]

    instance = None

    def get_form_instance(self, step):
        if self.instance is None:
            self.instance = Seminar()
            for form_key in self.get_form_list():
                self.get_form(
                    step=form_key,
                    data=self.storage.get_step_data(form_key),
                    files=self.storage.get_step_files(form_key)
                ).is_valid()
        return self.instance

    def get(self, *args, **kwargs):
        if 'reset' in self.request.GET:
            self.storage.reset()
            messages.info(self.request, "Seminaranmeldung abgebrochen")
            return HttpResponseRedirect('/')
        return super().get(*args, **kwargs)

    def get_form_kwargs(self, step=None):
        form_kwargs = super().get_form_kwargs(step=step)
        if step == 'group':
            form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_steps(self):
        forms = OrderedDict()
        for form_key in self.get_form_list():
            forms[form_key] = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
        return forms

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context['steps'] = self.get_steps()
        content = self.get_cleaned_data_for_step('content')
        if content:
            context['seminar_title'] = content['title']
        if self.steps.current == 'funding':
            context['max_funding'] = self.get_form_instance('funding').get_max_funding()
        return context

    def render_goto_step(self, goto_step, **kwargs):
        # try to save form
        form = self.get_form(data=self.request.POST, files=self.request.FILES)
        # if form.is_valid():
        self.storage.set_step_data(self.steps.current, self.process_step(form))
        self.storage.set_step_files(self.steps.current, self.process_step_files(form))
        return super().render_goto_step(goto_step, **kwargs)

    def done(self, form_list, **kwargs):
        self.instance.author = self.request.user
        self.instance.save()
        messages.success(self.request, 'Seminar "%s" gespeichert.' % self.instance.title)
        return render(self.request, 'seminars/seminar_wizard_done.html', {
            'instance': self.instance,
        })


class SeminarDeleteView(PermissionRequiredMixin, DeleteView):
    model = Seminar
    success_url = reverse_lazy('seminars:list')
    success_message = "Seminar „%(title)s“ wurde gelöscht."
    permission_required = 'seminars.delete_seminar'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message % self.get_object().__dict__)
        return super().delete(request, *args, **kwargs)


# TODO: UpdateView
