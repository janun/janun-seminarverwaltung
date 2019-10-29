from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django_tables2.views import SingleTableMixin

from backend.mixins import ErrorMessageMixin
from .models import User
from .forms import ProfileForm
from .tables import UserTable


class UserListView(SingleTableMixin, UserPassesTestMixin, ListView):
    model = User
    table_class = UserTable

    def test_func(self):
        if self.request.user.is_staff:
            return True


class UserCreateView(UserPassesTestMixin, CreateView):
    model = User

    def test_func(self):
        if self.request.user.is_staff:
            return True


class DetailView(
    ErrorMessageMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    success_message = "Deine Änderungen wurden gespeichert."
    success_url = reverse_lazy("users:detail")

    def test_func(self):
        if self.request.user.is_staff:
            return True


class ProfileView(ErrorMessageMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    success_message = "Deine Änderungen wurden gespeichert."
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user
