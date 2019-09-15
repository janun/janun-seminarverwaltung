import random

from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin
from django.contrib import messages

from backend.seminars.models import Seminar, JANUNGroup
from backend.seminars.forms import SeminarChangeForm


def get_greeting():
    greetings = ("Willkommen", "Hallo", "Guten Tag", "Hey", "Hi", "Moin", "Tach")
    return random.choice(greetings)


class Dashboard(ListView):
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


class SeminarDetailView(ModelFormMixin, DetailView):
    model = Seminar
    template_name = "dashboard/seminar_detail.html"
    form_class = SeminarChangeForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Deine Änderungen wurden gespeichert.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Es gab Probleme beim Speichern. Schau in’s Formular."
        )
        return super().form_invalid(form)


class JANUNGroupDetailView(DetailView):
    model = JANUNGroup
    template_name = "dashboard/group_detail.html"
