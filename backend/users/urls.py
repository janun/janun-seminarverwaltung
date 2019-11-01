from django.urls import path
from backend.users import views

app_name = "users"

urlpatterns = [
    path("", views.UserListView.as_view(), name="list"),
    path("add", views.UserCreateView.as_view(), name="add"),
    path("export", views.UserExportView.as_view(), name="export"),
    path("<slug:username>/", views.DetailView.as_view(), name="detail"),
    path("<slug:username>/delete", views.UserDeleteView.as_view(), name="delete"),
    path("<slug:username>/2fa", views.UserTwoFactorSetupView.as_view(), name="2fa"),
    path(
        "<slug:username>/2fa_remove",
        views.UserTwoFactorRemoveView.as_view(),
        name="2fa_remove",
    ),
]
