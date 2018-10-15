from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.JANUNGroupListView.as_view(), name='list'),
    path('create/', views.JANUNGroupCreateView.as_view(), name='create'),
    path('<int:pk>/', views.JANUNGroupDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.JANUNGroupDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.JANUNGroupUpdateView.as_view(), name='edit'),
]
