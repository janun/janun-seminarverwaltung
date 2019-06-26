from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
    path("accounts/", include("allauth.urls")),
]
