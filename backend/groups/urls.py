from django.urls import path
from . import views

app_name = "groups"

urlpatterns = [
    path("", views.JANUNGroupStaffListView.as_view(), name="staff_list"),
    path("add", views.JANUNGroupCreateView.as_view(), name="add"),
    path("export", views.JANUNGroupExportView.as_view(), name="export"),
    path("<slug:slug>", views.JANUNGroupDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit", views.JANUNGroupUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete", views.JANUNGroupDeleteView.as_view(), name="delete"),
]
