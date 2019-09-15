from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard.as_view(), name="list"),
    path(
        "seminars/<slug:slug>", views.SeminarDetailView.as_view(), name="seminar_detail"
    ),
]
