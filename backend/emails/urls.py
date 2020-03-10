from django.urls import path

from . import views

app_name = "emails"

urlpatterns = [
    path("", views.EmailTemplateListView.as_view(), name="list"),
    path("create", views.EmailTemplateCreateView.as_view(), name="create"),
    path("<int:pk>", views.EmailTemplateUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.EmailTemplateDeleteView.as_view(), name="delete"),
]
