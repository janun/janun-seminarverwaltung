from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
    path(
        "seminars/<int:year>/<slug:slug>",
        views.SeminarUpdateView.as_view(),
        name="seminar_detail",
    ),
    path(
        "groups/<slug:slug>", views.JANUNGroupDetailView.as_view(), name="group_detail"
    ),
]
