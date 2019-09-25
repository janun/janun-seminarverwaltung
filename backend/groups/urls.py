from django.urls import path
from . import views

urlpatterns = [
    path("<slug:slug>", views.JANUNGroupDetailView.as_view(), name="group_detail")
]
