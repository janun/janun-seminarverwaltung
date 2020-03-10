from django.urls import path
from backend.config import views

app_name = "config"


urlpatterns = [
    path("", views.GeneralSettingsView.as_view(), name="general"),
    path("funding", views.FundingRateListView.as_view(), name="funding_list"),
    path(
        "funding/<int:year>",
        views.FundingRateUpdateView.as_view(),
        name="funding_update",
    ),
    path(
        "funding/<int:year>/delete",
        views.FundingRateDeleteView.as_view(),
        name="funding_delete",
    ),
    path(
        "funding/create", views.FundingRateCreateView.as_view(), name="funding_create"
    ),
]
