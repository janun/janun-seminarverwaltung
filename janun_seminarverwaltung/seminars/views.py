from collections import OrderedDict

from django.views.generic import DetailView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import HttpResponseRedirect, Http404
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from rules.contrib.views import PermissionRequiredMixin
from braces.views import SelectRelatedMixin
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from formtools.wizard.views import NamedUrlSessionWizardView
from django_fsm import has_transition_perm

from seminars.models import Seminar
from seminars.tables import SeminarTable
from seminars.filters import SeminarFilter
import seminars.forms as seminar_forms
from .email import send_wizard_done_mails


class SeminarListView(SingleTableMixin, FilterView):
    model = Seminar
    table_class = SeminarTable
    filterset_class = SeminarFilter
    template_name = "seminars/seminar_list.html"
    paginate_by = 25
    strict = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orig_count = 0  # count before filter

    def get_queryset(self):
        qs = self.request.user.get_seminars()
        qs = qs.select_related('group', 'author')
        self.orig_count = qs.count()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        heading = "Deine Seminare"
        if user.role == "VERWALTER":
            heading = "Alle Seminare"
        elif user.group_hats.exists() or user.janun_groups.exists():
            heading += " und die Deiner Gruppen"

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
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['available_transitions'] = list(self.object.get_available_user_state_transitions(user))
        return context


class SeminarEditView(PermissionRequiredMixin, UpdateView):
    model = Seminar
    permission_required = 'seminars.edit_seminar'
    raise_exception = True
    fields = ('title', 'start', 'end', 'location', 'content',
              'planned_training_days', 'planned_attendees', 'requested_funding', 'group')
    template_name_suffix = '_edit_form'


class SeminarChangeStateView(DetailView):
    model = Seminar
    template_name = 'seminars/seminar_change_state.html'

    def __init__(self, *args, **kwargs):
        self.transition = None
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transition'] = self.transition
        return context

    def get(self, request, *args, **kwargs):
        transition_name = kwargs.get('transition', None)
        instance = self.get_object()
        possible_transitions = instance.get_available_state_transitions()
        try:
            self.transition = next(trans for trans in possible_transitions if trans.name == transition_name)
        except StopIteration:
            raise Http404
        transition_func = getattr(instance, transition_name)
        user = request.user
        if not has_transition_perm(transition_func, user):
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        transition_name = kwargs.get('transition', None)
        if transition_name:
            user = request.user
            instance = self.get_object()
            self.transition = getattr(instance, transition_name)
            if has_transition_perm(self.transition, user):
                self.transition()
                instance.save()
                messages.info(request, "Status wurde geändert auf \"%s\"" % instance.get_state_display())
            else:
                raise PermissionDenied
        return HttpResponseRedirect(instance.get_absolute_url())


class SeminarWizardView(NamedUrlSessionWizardView):
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
        form = self.get_form(data=self.request.POST, files=self.request.FILES)
        self.storage.set_step_data(self.steps.current, self.process_step(form))
        self.storage.set_step_files(self.steps.current, self.process_step_files(form))
        return super().render_goto_step(goto_step, **kwargs)

    def done(self, form_list, **kwargs):
        self.instance.author = self.request.user
        self.instance.save()
        messages.success(self.request, 'Seminar "{0}" gespeichert.'.format(self.instance.title))
        send_wizard_done_mails(seminar=self.instance, request=self.request)
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
