from collections import OrderedDict

from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

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


class SeminarDeleteView(SuccessMessageMixin, DeleteView):
    model = Seminar
    template_name = "seminars/seminar_delete.html"
    success_url = "/"
    success_message = "Das Seminar {} wurde gelöscht."

    def delete(self, request, *args, **kwargs):
        seminar_title = self.get_object().title
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message.format(seminar_title))
        return result


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
            form = self.get_form()
            if form.instance.title:
                messages.info(request, "Frühere Formulareingaben wiederhergestellt")
                return self.render(form)
        except KeyError:
            pass
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
            # TODO: Get form valid status for wizard steps
            # forms[form_key].is_valid() raises errors on wrong steps
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
            self.request, "seminars/seminar_apply_done.html", {"seminar": self.instance}
        )


# TODO: get only comments for seminars the user is allowed to see
class CommentListView(AjaxableResponseMixin, ListView):
    model = SeminarComment
    template_name = "seminars/_comment_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        seminar = get_object_or_404(Seminar, slug=self.kwargs["slug"])
        return seminar.comments.all()


# TODO: Allow to comment only on forms the user is allowed to access
class CommentCreateView(AjaxableResponseMixin, CreateView):
    model = SeminarComment
    fields = ("text",)
    success_url = "/"

    def form_valid(self, form):
        form.instance.seminar = get_object_or_404(Seminar, slug=self.kwargs["slug"])
        result = super().form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        return result


class CommentDeleteView(AjaxableResponseMixin, DeleteView):
    model = SeminarComment
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
