from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from rules.contrib.views import PermissionRequiredMixin
from django_tables2 import SingleTableView

from janun_seminarverwaltung.users.models import User
from users.tables import UserTable


class UserDetailView(PermissionRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    permission_required = 'users.detail_user'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.role == "PRUEFER":
            context['groups'] = self.object.group_hats.all()
        if self.object.role == "TEAMER":
            context['groups'] = self.object.janun_groups.all()
        return context


class UserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    fields = ["name"]
    model = User
    permission_required = 'users.detail_user'
    raise_exception = True

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


class UserListView(PermissionRequiredMixin, SingleTableView):
    model = User
    table_class = UserTable
    slug_field = "username"
    slug_url_kwarg = "username"
    permission_required = 'users.can_see_all_users'
    raise_exception = True

# TODO: UserDeleteView
