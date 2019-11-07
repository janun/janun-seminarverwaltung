from collections import OrderedDict

from django.views.generic import (
    View,
    TemplateView,
    ListView,
    FormView,
    DeleteView,
    UpdateView,
    CreateView,
)
from django.views.generic.base import RedirectView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse

from formtools.wizard.views import SessionWizardView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from tablib import Dataset

from backend.mixins import ErrorMessageMixin
from backend.utils import AjaxableResponseMixin
from backend.seminars import forms as seminar_forms

from .models import Seminar, SeminarComment, FundingRate
from .templateddocs import fill_template, FileResponse
from .tables import SeminarTable
from .filters import SeminarStaffFilter
from .resources import SeminarResource
from .forms import (
    SeminarImportForm,
    FundingRateForm,
    SeminarTeamerChangeForm,
    SeminarStaffChangeForm,
)


class FundingRateUpdateView(
    ErrorMessageMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView
):
    model = FundingRate
    form_class = FundingRateForm

    def get_success_message(self, request):
        return "Förderungssätze {} gespeichert.".format(self.kwargs["year"])

    def get_success_url(self):
        year = self.kwargs["year"]
        return reverse("seminars:list_staff", kwargs={"year": year})

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = self.kwargs["year"]
        return context

    def get_object(self):
        year = self.kwargs["year"]
        try:
            return FundingRate.objects.get(year=year)
        except FundingRate.DoesNotExist:
            return FundingRate(year=year)


class SeminarListView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_staff:
            return reverse("seminars:list_staff", args=[timezone.now().year])
        else:
            return reverse("seminars:list_yours")


class YourSeminarListView(ListView):
    model = Seminar
    context_object_name = "seminars"
    template_name = "seminars/your_seminars.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(owner=self.request.user)
            .select_related("owner", "group")
        )


class StaffSeminarListView(SingleTableMixin, UserPassesTestMixin, FilterView):
    model = Seminar
    filterset_class = SeminarStaffFilter
    context_object_name = "seminars"
    template_name = "seminars/staff_seminars.html"
    table_class = SeminarTable
    paginate_by = 50

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs["year"]
        context["current_year"] = year
        context["years"] = [
            d.year for d in Seminar.objects.dates("start_date", "year", order="DESC")
        ]
        context["confirmed_aggregates"] = (
            Seminar.objects.filter(start_date__year=year)
            .is_confirmed()
            .get_aggregates()
        )
        context["transferred_aggregates"] = Seminar.objects.filter(
            start_date__year=year, status="überwiesen"
        ).get_aggregates()
        context["bills_present_aggregates"] = (
            Seminar.objects.filter(start_date__year=year)
            .is_bills_present()
            .get_aggregates()
        )
        context["qs_aggregates"] = context["filter"].qs.get_aggregates()
        return context

    def get_queryset(self):
        year = self.kwargs["year"]
        return (
            super()
            .get_queryset()
            .filter(start_date__year=year)
            .select_related("owner", "group")
        )


class SeminarExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, *args, **kwargs):
        year = self.kwargs["year"]
        qs = Seminar.objects.filter(start_date__year=year).order_by("start_date")
        dataset = SeminarResource().export(qs)
        filename = "seminare_{}.csv".format(year)
        response = HttpResponse(dataset.csv, content_type="csv")
        response["Content-Disposition"] = "attachment; filename={}".format(filename)
        return response


class SeminarProofOfUseView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, *args, **kwargs):
        year = self.kwargs["year"]
        qs = Seminar.objects.filter(
            start_date__year=year, status="überwiesen"
        ).order_by("start_date")
        context = {"seminars": qs}
        odt_filepath = fill_template("seminars/verwendungsnachweis.odt", context)
        filename = "Verwendungsnachweis_{}.odt".format(year)
        return FileResponse(odt_filepath, filename)


# class SeminarImportView(ErrorMessageMixin, UserPassesTestMixin, FormView):
#     template_name = "seminars/import.html"
#     form_class = SeminarImportForm
#     resource_class = SeminarResource
#     success_url = "/seminars"

#     def test_func(self):
#         return self.request.user.is_staff

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["fields"] = [
#             f.column_name for f in self.resource_class().get_user_visible_fields()
#         ]
#         context["possible_status"] = Seminar.STATE_CHOICES._db_values
#         return context

#     def form_valid(self, form):
#         resource = self.resource_class()
#         dataset = Dataset()
#         dataset.load(self.request.FILES["file"].read().decode("utf-8"), format="csv")
#         result = resource.import_data(
#             dataset, dry_run=True, raise_errors=True, user=self.request.user
#         )

#         if not result.has_errors() and not result.has_validation_errors():
#             resource.import_data(dataset, dry_run=False)
#             messages.success(self.request, "Seminare erfolgreich importiert")
#             return super().form_valid(form)


def user_may_access_seminar(user, seminar):
    if user.is_superuser:
        return True
    if user == seminar.owner:
        return True
    if (
        seminar.group
        and user.is_reviewed
        and (
            seminar.group in user.janun_groups.all()
            or seminar.group in user.group_hats.all()
        )
    ):
        return True
    return False


class SeminarUpdateView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        year = kwargs["year"]
        slug = kwargs["slug"]
        if self.request.user.is_staff:
            return reverse("seminars:detail_staff", kwargs={"year": year, "slug": slug})
        else:
            return reverse("seminars:detail_teamer", kwargs={"year": year, "slug": slug})


class SeminarTeamerUpdateView(
    UserPassesTestMixin, ErrorMessageMixin, SuccessMessageMixin, UpdateView
):
    form_class = SeminarTeamerChangeForm
    queryset = Seminar.objects.select_related("owner", "group")
    template_name = "seminars/seminar_teamer_detail.html"
    success_message = "Deine Änderungen wurden gespeichert."

    def test_func(self):
        return user_may_access_seminar(self.request.user, self.get_object())

    def form_valid(self, form):
        # only owner may save
        if self.request.user != self.get_object().owner:
            raise PermissionDenied()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class SeminarStaffUpdateView(
    UserPassesTestMixin, ErrorMessageMixin, SuccessMessageMixin, UpdateView
):
    form_class = SeminarStaffChangeForm
    queryset = Seminar.objects.select_related("owner", "group")
    template_name = "seminars/seminar_staff_detail.html"
    success_message = "Deine Änderungen wurden gespeichert."

    def test_func(self):
        return self.request.user.is_staff

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class SeminarDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Seminar
    success_url = "/"
    success_message = "Das Seminar {} wurde gelöscht."

    def test_func(self):
        user = self.request.user
        seminar = self.get_object()
        if user.is_superuser:
            return True
        if user == seminar.owner and seminar.status == "angemeldet":
            return True

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
            try:
                forms[form_key].is_valid()
            except ValueError:
                pass
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
        email = self.request.user.email
        # TODO: Send mail
        return render(
            self.request,
            "seminars/seminar_apply_done.html",
            {"seminar": self.instance, "email": email},
        )


class SeminarApplyDoneTestView(TemplateView):
    template_name = "seminars/seminar_apply_done.html"


class CommentListView(AjaxableResponseMixin, ListView):
    model = SeminarComment
    template_name = "seminars/_comment_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        seminar = get_object_or_404(Seminar, slug=self.kwargs["slug"])
        if user_may_access_seminar(self.request.user, seminar):
            return seminar.comments.all()
        return SeminarComment.objects.none()


class CommentCreateView(AjaxableResponseMixin, CreateView):
    model = SeminarComment
    fields = ("text",)
    success_url = "/"

    def form_valid(self, form):
        seminar = get_object_or_404(Seminar, slug=self.kwargs["slug"])
        if not user_may_access_seminar(self.request.user, seminar):
            raise PermissionDenied()
        form.instance.seminar = seminar
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
