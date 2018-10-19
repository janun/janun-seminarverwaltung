from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash

from rules.contrib.views import PermissionRequiredMixin
from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from janun_seminarverwaltung.users.models import User
from users.tables import UserTable
from users.filters import UserFilter
from users.forms import UserCreationForm, UserChangeForm


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


class UserReviewView(PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_review.html'
    permission_required = 'users.review'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        is_reviewed = request.POST.get('is_reviewed', None)
        if is_reviewed:
            instance.is_reviewed = True
            instance.save()
            messages.info(request, "Benutzer_in wurde überprüft.")
        return HttpResponseRedirect(instance.get_absolute_url())


class UserDeactivateView(PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_deactivate.html'
    permission_required = 'users.deactivate_user'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        if instance.is_active:
            context['action_name'] = 'deactivate'
            context['action'] = "deaktivieren"
        else:
            context['action_name'] = 'activate'
            context['action'] = "reaktivieren"
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        deactivate = request.POST.get('deactivate', None)
        if deactivate:
            instance.is_active = False
            instance.save()
            messages.info(request, "Benutzer_in wurde deaktiviert.")
        activate = request.POST.get('activate', None)
        if activate:
            instance.is_active = True
            instance.save()
            messages.info(request, "Benutzer_in wurde reaktiviert.")
        return HttpResponseRedirect(instance.get_absolute_url())


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = UserChangeForm
    model = User
    permission_required = 'users.change_user'
    raise_exception = True
    template_name_suffix = '_edit'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs

    def form_valid(self, form):
        return_value = super().form_valid(form)
        update_session_auth_hash(self.request, form.instance)
        return return_value


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
    form_class = UserCreationForm
    permission_required = 'users.add_user'
    raise_exception = True
    template_name_suffix = '_create'

    # https://github.com/dfunckt/django-rules/issues/85
    def get_object(self):
        return None

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs['autofocus'] = True
        return form
