import random

from django.views.generic import ListView, DetailView

from backend.seminars.models import Seminar


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


class SeminarDetailView(DetailView):
    model = Seminar
    template_name = "dashboard/seminar_detail.html"
