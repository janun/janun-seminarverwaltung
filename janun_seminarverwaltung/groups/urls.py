from django.urls import path
from .views import JANUNGroupListView, JANUNGroupDetailView, JANUNGroupCreateView, JANUNGroupDeleteView

app_name = 'groups'

urlpatterns = [
    path('', JANUNGroupListView.as_view(), name='list'),
    path('create', JANUNGroupCreateView.as_view(), name='create'),
    path('<int:pk>/', JANUNGroupDetailView.as_view(), name='detail'),
    path('<int:pk>/delete', JANUNGroupDeleteView.as_view(), name='delete'),
]
