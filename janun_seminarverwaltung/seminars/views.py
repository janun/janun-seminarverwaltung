from django.views.generic import DetailView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.core import validators

from rules.contrib.views import PermissionRequiredMixin
# from braces.views import SelectRelatedMixin
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from formtools.wizard.views import NamedUrlSessionWizardView

from seminars.models import Seminar, calc_max_funding
from seminars.tables import SeminarTable
from seminars.filters import SeminarFilter
import seminars.forms as seminar_forms


class SeminarListView(FilterView, SingleTableView):
    model = Seminar
    table_class = SeminarTable
    filterset_class = SeminarFilter
    template_name = "seminars/seminar_list.html"

    def get_queryset(self):
        if self.request.user.role == "TEAMER":
            qs = Seminar.objects.filter(author=self.request.user)
            self.orig_len = qs.count()
            return qs
        if self.request.user.role == "PRUEFER":
            qs = Seminar.objects.filter(
                group__in=self.request.user.group_hats.all()
            )
            self.orig_len = qs.count()
            return qs
        if self.request.user.role == "VERWALTER":
            qs = Seminar.objects.all()
            self.orig_len = qs.count()
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == "TEAMER":
            context['heading'] = "Deine Seminare (%s)" % self.orig_len
        if self.request.user.role == "PRUEFER":
            context['heading'] = "Seminare deiner Gruppen (%s)" % len(self.object_list)
        if self.request.user.role == "VERWALTER":
            context['heading'] = "Alle Seminare (%s)" % len(self.object_list)
        context['orig_len'] = self.orig_len
        return context


class SeminarDetailView(PermissionRequiredMixin, DetailView):
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
        return self.instance

    # def get_form_kwargs(self, step=None):
    #     form_kwargs = super().get_form_kwargs(step=step)
    #     return form_kwargs

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        # set initial group if only one possibility
        if step == 'group':
            if self.request.user.role == 'TEAMER' and self.request.user.janun_groups.count() == 1:
                initial['group'] = self.request.user.janun_groups.get()
        return initial

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step=step, data=data, files=files)
        if step is None:
            step = self.steps.current
        # TEAMER may only choose own groups
        if step == 'group':
            if self.request.user.role == 'TEAMER':
                form.fields['group'].queryset = self.request.user.janun_groups
        if step == 'days':
            max_training_days = self.get_max_training_days()
            if max_training_days:
                form.fields['planned_training_days'].validators.append(
                    validators.MaxValueValidator(max_training_days)
                )
        # funding may not be higher than max_funding
        if step == 'funding':
            max_funding = self.get_max_funding()
            if max_funding:
                form.fields['requested_funding'].validators.append(
                    validators.MaxValueValidator(max_funding)
                )
            else:
                form.fields['requested_funding'].validators.append(
                    validators.MaxValueValidator(
                        0,
                        message="Du musst Gruppe, Bildungstage und Teilnehmende ausfüllen."
                    )
                )
        return form

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        content = self.get_cleaned_data_for_step('content')
        if content:
            context['seminar_title'] = content['title']
        if self.steps.current == 'funding':
            context['max_funding'] = self.get_max_funding()
        return context

    def render_goto_step(self, goto_step, **kwargs):
        # try to save form
        form = self.get_form(data=self.request.POST, files=self.request.FILES)
        if form.is_valid():
            self.storage.set_step_data(self.steps.current, self.process_step(form))
            self.storage.set_step_files(self.steps.current, self.process_step_files(form))
        return super().render_goto_step(goto_step, **kwargs)

    def done(self, form_list, **kwargs):
        self.instance.author = self.request.user
        self.instance.save()
        messages.success(self.request, 'Seminar "%s" gespeichert.' % self.instance.title)
        return HttpResponseRedirect('/')

    def get_max_funding(self):
        group = self.get_cleaned_data_for_step('group')
        days = self.get_cleaned_data_for_step('days')
        attendees = self.get_cleaned_data_for_step('attendees')
        if group is not None and days is not None and attendees is not None:
            return calc_max_funding(
                days['planned_training_days'],
                attendees['planned_attendees'].upper,
                group['group'] != ''
            )
        return None

    def get_max_training_days(self):
        datetime_data = self.get_cleaned_data_for_step('datetime')
        if datetime_data:
            start = datetime_data['start']
            end = datetime_data['end']
            return (end - start).days + 1
        return None

# TODO: DeleteView, UpdateView
