from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages


from .models import User
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "account/profile.html"
    success_message = "Deine Änderungen wurden gespeichert."
    error_message = "Es gab Probleme beim Speichern. Schau in’s Formular."

    def get_success_url(self):
        return reverse("account_profile")

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)

    def get_object(self):
        return self.request.user
