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

from backend.mixins import ErrorMessageMixin, StaffOnlyMixin
from backend.utils import AjaxableResponseMixin
from backend.seminars import forms as seminar_forms
from backend.emails.models import EmailTemplate

from .models import Seminar, SeminarComment, get_max_funding, SeminarView
from .templateddocs import fill_template, FileResponse
from .tables import SeminarTable, SeminarHistoryTable
from .filters import SeminarStaffFilter
from .resources import SeminarResource
from .forms import (
    SeminarImportForm,
    SeminarTeamerChangeForm,
    SeminarStaffChangeForm,
    SeminarTeamerApplyForm,
)


class CalcMaxFundingView(View):
    """Helper ajax view for seminar application"""

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


class StaffSeminarListView(SingleTableMixin, StaffOnlyMixin, FilterView):
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


class SeminarExportView(StaffOnlyMixin, View):
    """Export all seminars of a certain year as a CSV file"""

    def get(self, *args, **kwargs):
        year = self.kwargs["year"]
        qs = Seminar.objects.filter(start_date__year=year).order_by("start_date")
        dataset = SeminarResource().export(qs)
        filename = "seminare_{}.csv".format(year)
        response = HttpResponse(dataset.csv, content_type="csv")
        response["Content-Disposition"] = "attachment; filename={}".format(filename)
        return response


class SeminarProofOfUseView(StaffOnlyMixin, View):
    """Generates the Verwendungsnachweis for a certain year containing all seminars that are überwiesen"""

    @staticmethod
    def batch_seminars(qs, n):
        """Return seminars in batches of size n

        Also adds running sums

        Args:
            qs: Queryset containing seminars
            n: size of batches
        Returns:
            Generator of seminars in batches
        """

        class L(list):
            pass

        l = len(qs)
        tnt_sum = 0
        tnt_sum_jfg = 0
        funding_sum = 0
        expense_sum = 0
        income_sum = 0
        offset = 0
        for ndx in range(0, l, n):
            batch = L(qs[ndx : min(ndx + n, l)])
            batch.offset = offset
            offset += n

            tnt_sum += sum(s.actual_attendence_days_total for s in batch)
            batch.tnt_sum = tnt_sum

            tnt_sum_jfg += sum(s.actual_attendence_days_jfg for s in batch)
            batch.tnt_sum_jfg = tnt_sum_jfg

            expense_sum += sum(s.expense_total for s in batch)
            batch.expense_sum = expense_sum

            income_sum += sum(s.income_total for s in batch)
            batch.income_sum = income_sum

            funding_sum += sum(s.actual_funding for s in batch)
            batch.funding_sum = funding_sum
            yield batch

    def get(self, *args, **kwargs):
        year = self.kwargs["year"]
        qs = (
            Seminar.objects.filter(start_date__year=year, status="überwiesen")
            .annotate_expense_total()
            .annotate_income_total()
            .order_by("start_date")
        )
        batched_seminars = list(self.batch_seminars(qs, 15))
        context = {"seminars": qs, "batched_seminars": batched_seminars}
        odt_filepath = fill_template("seminars/verwendungsnachweis.odt", context)
        filename = "Verwendungsnachweis_{}.odt".format(year)
        return FileResponse(odt_filepath, filename)


class SeminarImportView(ErrorMessageMixin, StaffOnlyMixin, FormView):
    template_name = "seminars/import.html"
    form_class = SeminarImportForm
    resource_class = SeminarResource
    success_url = "/seminars"

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
        # dry run first
        result = resource.import_data(
            dataset,
            dry_run=True,
            raise_errors=False,
            user=self.request.user,
            use_transactions=True,
        )
        # success
        if not result.has_errors() and not result.has_validation_errors():
            resource.import_data(dataset, dry_run=False, use_transactions=True)
            messages.success(self.request, "Seminare erfolgreich importiert")
            return super().form_valid(form)
        # error handling
        else:
            messages.error(
                self.request, "Fehler beim Importieren, schau unten nach Details."
            )
            context = self.get_context_data()
            context["invalid_rows"] = result.invalid_rows
            context["row_errors"] = result.row_errors
            return render(self.request, self.template_name, context=context)


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
        seminar = self.get_object()
        if self.request.user != seminar.owner:
            raise PermissionDenied()
        result = super().form_valid(form)
        newseminar = self.get_object()
        EmailTemplate.send(
            "seminar_update",
            {"seminar_old": seminar, "seminar": newseminar, "user": self.request.user,},
        )
        return result

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class SeminarHistoryView(StaffOnlyMixin, TemplateView):
    template_name = "seminars/seminar_history.html"

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
    StaffOnlyMixin, ErrorMessageMixin, SuccessMessageMixin, UpdateView
):
    form_class = SeminarStaffChangeForm
    queryset = Seminar.objects.annotate_deadline_status().select_related(
        "owner", "group"
    )
    template_name = "seminars/seminar_staff_detail.html"
    success_message = "Deine Änderungen wurden gespeichert."

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        SeminarView(user=self.request.user, seminar=self.object).save()
        return response

    def form_valid(self, *args, **kwargs):
        oldseminar = self.get_object()
        result = super().form_valid(*args, **kwargs)
        newseminar = self.get_object()
        EmailTemplate.send(
            "seminar_update",
            {
                "seminar_old": oldseminar,
                "seminar": newseminar,
                "user": self.request.user,
            },
        )
        return result

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
        seminar = self.get_object()
        messages.success(self.request, self.success_message.format(seminar.title))
        EmailTemplate.send(
            "seminar_delete", {"user": self.request.user, "seminar": seminar},
        )
        result = super().delete(request, *args, **kwargs)
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

    def form_valid(self, form):
        result = super().form_valid(form)
        # send mail
        EmailTemplate.send(
            "seminar_applied", {"user": self.request.user, "seminar": self.object}
        )
        return result

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
