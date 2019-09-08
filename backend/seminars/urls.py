from django.urls import path
from .views import SeminarListView

urlpatterns = [path("", SeminarListView.as_view(), name="list")]
