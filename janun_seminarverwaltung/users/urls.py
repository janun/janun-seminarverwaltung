from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.UserListView.as_view(), name='list'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('~redirect/', views.UserRedirectView.as_view(), name='redirect'),
    # path('~update', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='edit'),

]
