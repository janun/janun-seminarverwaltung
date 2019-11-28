from collections import OrderedDict

from django.views.generic import (
    View,
    TemplateView,
    ListView,
    FormView,
    DeleteView,
    UpdateView,
    CreateView,
    DetailView,
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

from tablib import Dataset
from formtools.wizard.views import SessionWizardView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from backend.mixins import ErrorMessageMixin
from backend.utils import AjaxableResponseMixin
from backend.seminars import forms as seminar_forms

from .models import Seminar, SeminarComment, FundingRate, get_max_funding, SeminarView
from .templateddocs import fill_template, FileResponse
from .tables import SeminarTable, SeminarHistoryTable
from .filters import SeminarStaffFilter
from .resources import SeminarResource
from .forms import (
    SeminarImportForm,
    FundingRateForm,
    SeminarTeamerChangeForm,
    SeminarStaffChangeForm,
    SeminarTeamerApplyForm,
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


class CalcMaxFundingView(View):
    def get(self, request):
        year = int(request.GET.get("year", None))
        group = bool(request.GET.get("group", None))
        planned_training_days = int(request.GET.get("days", None))
        planned_attendees_max = int(request.GET.get("attendees", None))
        max_funding = get_max_funding(
            year, group, planned_training_days, planned_attendees_max
        )
        return HttpResponse(str(max_funding))


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
    queryset = (
        Seminar.objects.all()
        .annotate_tnt()
        .annotate_funding()
        .annotate_deadline_status()
        .select_related("owner", "group")
    )
    context_object_name = "seminars"
    template_name = "seminars/your_seminars.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class StaffSeminarListView(SingleTableMixin, UserPassesTestMixin, FilterView):
    model = Seminar
    queryset = (
        Seminar.objects.all()
        .annotate_tnt()
        .annotate_funding()
        .annotate_tnt_cost()
        .annotate_deadline_status()
        .select_related("owner", "group")
    )
    filterset_class = SeminarStaffFilter
    context_object_name = "seminars"
    template_name = "seminars/staff_seminars.html"
    table_class = SeminarTable
    paginate_by = 50

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get("year", None)
        context["current_year"] = year
        context["years"] = [
            d.year for d in Seminar.objects.dates("start_date", "year", order="DESC")
        ]
        if year:
            context["confirmed_aggregates"] = (
                Seminar.objects.filter(start_date__year=year)
                .is_confirmed()
                .get_aggregates()
            )
            context["confirmed_aggregates"]["tnt_cost"] = 0.0
            if context["confirmed_aggregates"]["tnt_sum"]:
                context["confirmed_aggregates"]["tnt_cost"] = (
                    context["confirmed_aggregates"]["funding_sum"]
                    / context["confirmed_aggregates"]["tnt_sum"]
                )
            context["transferred_aggregates"] = Seminar.objects.filter(
                start_date__year=year, status="überwiesen"
            ).get_aggregates()
            context["deadline_expired_aggregates"] = (
                Seminar.objects.annotate_deadline_status()
                .filter(start_date__year=year, deadline_status="expired")
                .get_aggregates()
            )
            context["bills_present_aggregates"] = (
                Seminar.objects.filter(start_date__year=year)
                .is_bills_present()
                .get_aggregates()
            )
        context["qs_aggregates"] = context["filter"].qs.get_aggregates()
        return context

    def get_queryset(self):
        year = self.kwargs.get("year", None)
        if year:
            return super().get_queryset().filter(start_date__year=year)
        return super().get_queryset()


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
        qs = (
            Seminar.objects.filter(start_date__year=year, status="überwiesen")
            .annotate_expense_total()
            .annotate_income_total()
            .order_by("start_date")
        )
        context = {"seminars": qs}
        odt_filepath = fill_template("seminars/verwendungsnachweis.odt", context)
        filename = "Verwendungsnachweis_{}.odt".format(year)
        return FileResponse(odt_filepath, filename)


class SeminarImportView(ErrorMessageMixin, UserPassesTestMixin, FormView):
    template_name = "seminars/import.html"
    form_class = SeminarImportForm
    resource_class = SeminarResource
    success_url = "/seminars"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fields"] = [
            f.column_name for f in self.resource_class().get_user_visible_fields()
        ]
        context[
            "possible_status"
        ] = Seminar.STATE_CHOICES._db_values  # pylint: disable=protected-access
        return context

    def form_valid(self, form):
        resource = self.resource_class()
        dataset = Dataset()
        dataset.load(self.request.FILES["file"].read().decode("utf-8"), format="csv")
        result = resource.import_data(
            dataset, dry_run=True, raise_errors=True, user=self.request.user
        )

        if not result.has_errors() and not result.has_validation_errors():
            resource.import_data(dataset, dry_run=False)
            messages.success(self.request, "Seminare erfolgreich importiert")
            return super().form_valid(form)


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
            return reverse(
                "seminars:detail_teamer", kwargs={"year": year, "slug": slug}
            )


class SeminarTeamerUpdateView(
    UserPassesTestMixin, ErrorMessageMixin, SuccessMessageMixin, UpdateView
):
    form_class = SeminarTeamerChangeForm
    queryset = Seminar.objects.annotate_deadline_status().select_related(
        "owner", "group"
    )
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


class SeminarHistoryView(UserPassesTestMixin, TemplateView):
    template_name = "seminars/seminar_history.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seminar = get_object_or_404(
            Seminar, slug=self.kwargs["slug"], start_date__year=self.kwargs["year"]
        )
        history = seminar.history.all().select_related("history_user")
        context["seminar"] = seminar
        context["history_table"] = SeminarHistoryTable(history)
        return context


class SeminarStaffUpdateView(
    UserPassesTestMixin, ErrorMessageMixin, SuccessMessageMixin, UpdateView
):
    form_class = SeminarStaffChangeForm
    queryset = Seminar.objects.annotate_deadline_status().select_related(
        "owner", "group"
    )
    template_name = "seminars/seminar_staff_detail.html"
    success_message = "Deine Änderungen wurden gespeichert."

    def test_func(self):
        return self.request.user.is_staff

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        SeminarView(user=self.request.user, seminar=self.object).save()
        return response

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


class SeminarApplyDoneView(DetailView):
    template_name = "seminars/seminar_apply_done.html"

    def get_object(self):
        year = self.kwargs.get("year")
        slug = self.kwargs.get("slug")
        return get_object_or_404(Seminar, start_date__year=year, slug=slug)


class SeminarApplyView(ErrorMessageMixin, CreateView):
    form_class = SeminarTeamerApplyForm
    queryset = Seminar.objects.select_related("owner", "group")
    template_name = "seminars/seminar_teamer_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        seminar = self.object
        return reverse(
            "seminars:apply_done",
            kwargs={"year": seminar.start_date.year, "slug": seminar.slug},
        )


class SeminarApplyWizardView(SessionWizardView):
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


class CommentListView(ListView):
    model = SeminarComment
    template_name = "seminars/_comment_list.html"
    context_object_name = "comments"

    def get_queryset(self):
        seminar = get_object_or_404(
            Seminar.objects.select_related("owner"), slug=self.kwargs["slug"]
        )
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
        form.instance.owner = self.request.user
        result = super().form_valid(form)
        return result


class CommentDeleteView(AjaxableResponseMixin, DeleteView):
    model = SeminarComment
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
