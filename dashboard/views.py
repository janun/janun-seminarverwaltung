import random

from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from backend.seminars.models import Seminar
from backend.groups.models import JANUNGroup
from backend.seminars.forms import SeminarChangeForm


def get_greeting():
    greetings = ("Willkommen", "Hallo", "Guten Tag", "Hey", "Hi", "Moin", "Tach")
    return random.choice(greetings)


class Dashboard(LoginRequiredMixin, ListView):
    model = Seminar
    context_object_name = "seminars"
    template_name = "dashboard/dashboard.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["greeting"] = get_greeting()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class SeminarUpdateView(LoginRequiredMixin, UpdateView):
    queryset = Seminar.objects.select_related("owner", "group").prefetch_related(
        "comments"
    )
    template_name = "dashboard/seminar_detail.html"
    form_class = SeminarChangeForm
    success_message = "Deine Änderungen wurden gespeichert."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Es gab Probleme beim Speichern. Schau in’s Formular."
        )
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(is_internal=False)
        return context


class JANUNGroupDetailView(LoginRequiredMixin, DetailView):
    model = JANUNGroup
    template_name = "dashboard/group_detail.html"
