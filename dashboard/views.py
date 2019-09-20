import random

from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    DeleteView,
    CreateView,
)
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from backend.seminars.models import Seminar, SeminarComment
from backend.groups.models import JANUNGroup
from backend.seminars.forms import SeminarChangeForm
from backend.utils import AjaxableResponseMixin


def get_greeting():
    greetings = ("Willkommen", "Hallo", "Guten Tag", "Hey", "Hi", "Moin", "Tach")
    return random.choice(greetings)


class Dashboard(TemplateView):
    context_object_name = "seminars"
    template_name = "dashboard/dashboard.html"
    seminar_limit = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["greeting"] = get_greeting()
        context["janun_groups"] = self.request.user.janun_groups.all()
        context["group_hats"] = self.request.user.group_hats.all()
        context["seminars"] = self.request.user.seminars.all()[: self.seminar_limit]
        context["show_more_link"] = (
            self.request.user.seminars.count() > self.seminar_limit
        )
        return context


class SeminarListView(ListView):
    model = Seminar
    context_object_name = "seminars"
    template_name = "dashboard/seminars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class SeminarUpdateView(UpdateView):
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


class JANUNGroupDetailView(DetailView):
    model = JANUNGroup
    template_name = "dashboard/group_detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seminars_next_year"] = self.object.seminars.next_year().order_by(
            "start_date"
        )
        context["stats_next_year"] = (
            context["seminars_next_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        context["seminars_this_year"] = self.object.seminars.this_year().order_by(
            "start_date"
        )
        context["stats_this_year"] = (
            context["seminars_this_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        context["seminars_last_year"] = self.object.seminars.last_year().order_by(
            "start_date"
        )
        context["stats_last_year"] = (
            context["seminars_last_year"]
            .is_not_rejected()
            .aggregate(tnt_sum=Sum("tnt"), funding_sum=Sum("funding"))
        )
        return context


class CommentDeleteView(AjaxableResponseMixin, DeleteView):
    model = SeminarComment
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
