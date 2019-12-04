from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


class ErrorMessageMixin:
    error_message = "Es gab Probleme beim Speichern, schau ins Formular."

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = self.get_error_message()
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self):
        return self.error_message


class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_staff


class SuperuserOnlyMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_superuser
