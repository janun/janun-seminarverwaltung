from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
    path("history", views.GlobalHistoryView.as_view(), name="history"),
]
