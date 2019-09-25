from collections import OrderedDict

from django.views.generic import ListView, DeleteView, UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin

from formtools.wizard.views import SessionWizardView

from backend.mixins import ErrorMessageMixin
from backend.seminars.models import Seminar, SeminarComment
from backend.seminars.forms import SeminarChangeForm
from backend.utils import AjaxableResponseMixin
from backend.seminars import forms as seminar_forms


class SeminarListView(ListView):
    model = Seminar
    context_object_name = "seminars"
    template_name = "seminars/seminars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class SeminarUpdateView(ErrorMessageMixin, SuccessMessageMixin, UpdateView):
    form_class = SeminarChangeForm
    queryset = Seminar.objects.select_related("owner", "group").prefetch_related(
        "comments"
    )
    template_name = "seminars/seminar_detail.html"
    success_message = "Deine Änderungen wurden gespeichert."
    error_message = "Es gab Probleme beim Speichern. Schau in’s Formular."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(is_internal=False)
        return context


class CommentDeleteView(AjaxableResponseMixin, DeleteView):
    model = SeminarComment
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class SeminarApplyView(SessionWizardView):
    template_name = "seminars/seminar_apply.html"
    form_list = [
        seminar_forms.ContentSeminarForm,
        seminar_forms.DateLocationSeminarForm,
        seminar_forms.GroupSeminarForm,
        seminar_forms.TrainingDaysSeminarForm,
        seminar_forms.AttendeesSeminarForm,
        seminar_forms.FundingSeminarForm,
        seminar_forms.ConfirmSeminarForm,
    ]

    def get(self, request, *args, **kwargs):
        try:
            # restore saved steps
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)

    def get_form_instance(self, step):
        if not getattr(self, "instance", None):
            self.instance = Seminar()
            for form_key in self.get_form_list():
                self.get_form(
                    step=form_key,
                    data=self.storage.get_step_data(form_key),
                    files=self.storage.get_step_files(form_key),
                ).is_valid()
        return self.instance

    def get_steps(self):
        forms = OrderedDict()
        for form_key in self.get_form_list():
            forms[form_key] = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key),
            )
        return forms

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context["steps"] = self.get_steps()
        return context

    def done(self, form_list, **kwargs):
        self.instance.owner = self.request.user
        self.instance.save()
        return render(
            self.request,
            "seminars/seminar_apply_done.html",
            {"instance": self.instance},
        )


class ApplyDoneTestView(TemplateView):
    template_name = "seminars/seminar_apply_done.html"
