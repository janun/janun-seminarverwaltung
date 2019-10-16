from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from backend.mixins import ErrorMessageMixin
from .models import User
from .forms import ProfileForm


class ProfileView(ErrorMessageMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    success_message = "Deine Änderungen wurden gespeichert."
    error_message = "Es gab Probleme beim Speichern. Schau in’s Formular."
    success_url = reverse_lazy("account_profile")

    def get_object(self):
        return self.request.user
