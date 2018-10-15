from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from rules.contrib.views import PermissionRequiredMixin
from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from janun_seminarverwaltung.users.models import User
from users.tables import UserTable
from users.filters import UserFilter
from users.forms import UserCreateForm


class UserDetailView(PermissionRequiredMixin, DetailView):
    model = User
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
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = UserCreateForm
    model = User
    permission_required = 'users.change_user'
    raise_exception = True
    template_name_suffix = '_edit'


class UserListView(PermissionRequiredMixin, SingleTableMixin, FilterView):
    model = User
    table_class = UserTable
    filterset_class = UserFilter
    permission_required = 'users.see_all_users'
    raise_exception = True
    template_name = "users/user_list.html"
    paginate_by = 25
    strict = False


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'users.delete_user'
    raise_exception = True
    success_url = reverse_lazy('users:list')


class UserCreateView(PermissionRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    permission_required = 'users.add_user'
    raise_exception = True
    template_name_suffix = '_create'

    # https://github.com/dfunckt/django-rules/issues/85
    def get_object(self):
        return None
