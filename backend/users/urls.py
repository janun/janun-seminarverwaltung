from django.urls import include, path

from backend.users.views import ProfileView


urlpatterns = [
    path("", include("allauth.urls")),
    path("profile", ProfileView.as_view(), name="account_profile"),
    path("", include("allauth_2fa.urls")),
    path("", include("allauth.urls")),
]
