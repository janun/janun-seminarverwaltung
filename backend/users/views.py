from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from allauth_2fa.views import TwoFactorSetup, TwoFactorRemove
from allauth_2fa.utils import user_has_valid_totp_device
from django_otp.plugins.otp_totp.models import TOTPDevice

from django_tables2.views import SingleTableMixin

from backend.mixins import ErrorMessageMixin
from .models import User
from .forms import ProfileForm, UserDetailForm, UserCreateForm, UserTOTPDeviceRemoveForm
from .tables import UserTable
from .resources import UserResource


class UserListView(SingleTableMixin, UserPassesTestMixin, ListView):
    model = User
    table_class = UserTable

    def test_func(self):
        return self.request.user.is_staff


class UserCreateView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/user_create.html"
    success_message = "Konto erstellt"

    def test_func(self):
        return self.request.user.is_superuser


class UserDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:list")
    success_message = "Das Konto {} wurde gelöscht."
    slug_field = "username"
    slug_url_kwarg = "username"

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        username = self.get_object().username
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message.format(username))
        return result


class DetailView(
    ErrorMessageMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserDetailForm
    template_name = "users/user_detail.html"
    success_message = "Änderungen am Konto {} wurden gespeichert."
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_success_message(self, request):
        return self.success_message.format(self.get_object().username)

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.get_object().username})

    def test_func(self):
        return self.request.user.is_staff

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["request"] = self.request
        return form_kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            raise PermissionDenied()
        return super().form_valid(form)


class ProfileView(ErrorMessageMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    success_message = "Deine Änderungen wurden gespeichert."
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["request"] = self.request
        return form_kwargs


class UserTwoFactorSetupView(UserPassesTestMixin, TwoFactorSetup):
    template_name = "users/user_2fa_setup.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.get_object().username})

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def dispatch(self, request, *args, **kwargs):
        if user_has_valid_totp_device(self.get_object()):
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def _new_device(self):
        self.get_object().totpdevice_set.filter(confirmed=False).delete()
        self.device = TOTPDevice.objects.create(user=self.get_object(), confirmed=False)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, "2FA für {} eingerichtet.".format(self.get_object().username)
        )
        return result


class UserTwoFactorRemoveView(UserPassesTestMixin, TwoFactorRemove):
    template_name = "users/user_2fa_remove.html"
    form_class = UserTOTPDeviceRemoveForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.get_object().username})

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, "2FA für {} ausgeschaltet.".format(self.get_object().username)
        )
        return result


class UserExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        qs = User.objects.all()
        dataset = UserResource().export(qs)
        filename = "users.csv"
        response = HttpResponse(dataset.csv, content_type="csv")
        response["Content-Disposition"] = "attachment; filename={}".format(filename)
        return response
