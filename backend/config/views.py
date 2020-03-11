from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from django_tables2.views import SingleTableMixin

from backend.users.models import JANUNSeminarPreferences
from backend.seminars.models import FundingRate
from backend.mixins import ErrorMessageMixin, SuperuserOnlyMixin

from .forms import SettingsForm, FundingRateForm
from .tables import FundingRateTable


class GeneralSettingsView(SuccessMessageMixin, SuperuserOnlyMixin, UpdateView):
    template_name = "config/general.html"
    model = JANUNSeminarPreferences
    success_message = "Gespeichert"
    form_class = SettingsForm
    success_url = reverse_lazy("config:general")

    def get_object(self):
        return JANUNSeminarPreferences.singleton.get()


class FundingRateListView(SingleTableMixin, SuperuserOnlyMixin, ListView):
    model = FundingRate
    template_name = "config/fundingrate_list.html"
    table_class = FundingRateTable


class FundingRateUpdateView(
    ErrorMessageMixin, SuccessMessageMixin, SuperuserOnlyMixin, UpdateView
):
    model = FundingRate
    form_class = FundingRateForm
    success_message = "Gespeichert"
    slug_field = "year"
    slug_url_kwarg = "year"
    template_name = "config/fundingrate_form.html"


class FundingRateCreateView(
    ErrorMessageMixin, SuccessMessageMixin, SuperuserOnlyMixin, CreateView
):
    model = FundingRate
    success_message = "Erstellt"
    form_class = FundingRateForm
    template_name = "config/fundingrate_form.html"


class FundingRateDeleteView(SuccessMessageMixin, SuperuserOnlyMixin, DeleteView):
    model = FundingRate
    success_url = reverse_lazy("config:funding_list")
    success_message = "{} wurde gelöscht."
    slug_field = "year"
    slug_url_kwarg = "year"
    template_name = "config/fundingrate_confirm_delete.html"
