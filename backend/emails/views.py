from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db import transaction

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from backend.mixins import SuperuserOnlyMixin

from .models import EmailTemplate
from .tables import EmailTemplateTable
from .forms import EmailTemplateForm, AttachmentFormset, ConditionFormset
from .filters import EmailTemplateFilter


class EmailTemplateListView(SingleTableMixin, SuperuserOnlyMixin, FilterView):
    model = EmailTemplate
    filterset_class = EmailTemplateFilter
    table_class = EmailTemplateTable
    template_name = "emails/emailtemplate_list.html"


class EmailTemplateUpdateView(SuccessMessageMixin, SuperuserOnlyMixin, UpdateView):
    model = EmailTemplate
    success_message = "Änderung gespeichert."
    form_class = EmailTemplateForm
    template_name = "emails/emailtemplate_update.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["attachments"] = AttachmentFormset(
                self.request.POST, self.request.FILES, instance=self.object
            )
            data["conditions"] = ConditionFormset(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["attachments"] = AttachmentFormset(instance=self.object)
            data["conditions"] = ConditionFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attachments = context["attachments"]
        conditions = context["conditions"]
        with transaction.atomic():
            self.object = form.save()
            if attachments.is_valid():
                attachments.instance = self.object
                attachments.save()
            if conditions.is_valid():
                conditions.instance = self.object
                conditions.save()
        return super().form_valid(form)


class EmailTemplateDeleteView(SuccessMessageMixin, SuperuserOnlyMixin, DeleteView):
    model = EmailTemplate
    success_url = reverse_lazy("emails:list")
    success_message = "E-Mail-Vorlage wurde gelöscht."


class EmailTemplateCreateView(SuccessMessageMixin, SuperuserOnlyMixin, CreateView):
    model = EmailTemplate
    success_message = "Erstellt."
    form_class = EmailTemplateForm
    template_name = "emails/emailtemplate_create.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["attachments"] = AttachmentFormset(
                self.request.POST, self.request.FILES
            )
            data["conditions"] = ConditionFormset(self.request.POST, self.request.FILES)
        else:
            data["attachments"] = AttachmentFormset()
            data["conditions"] = ConditionFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attachments = context["attachments"]
        conditions = context["conditions"]
        with transaction.atomic():
            self.object = form.save()
            if attachments.is_valid():
                attachments.instance = self.object
                attachments.save()
            if conditions.is_valid():
                conditions.instance = self.object
                conditions.save()
        return super().form_valid(form)
