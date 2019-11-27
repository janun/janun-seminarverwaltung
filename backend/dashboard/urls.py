from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
    path("history", views.GlobalHistoryView.as_view(), name="history"),
    path("search", views.SearchView.as_view(), name="search"),
    path("last_viewed", views.LastViewedSeminarsView.as_view(), name="last_viewed"),
]
