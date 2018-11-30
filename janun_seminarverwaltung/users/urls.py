from django.urls import path
from django.views.generic import TemplateView


from . import views

app_name = 'users'
urlpatterns = [
    path('', views.UserListView.as_view(), name='list'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('~redirect/', views.UserRedirectView.as_view(), name='redirect'),
    # path('~update', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
    path('<int:pk>/deactivate/', views.UserDeactivateView.as_view(), name='deactivate'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='edit'),
    path('<int:pk>/review/', views.UserReviewView.as_view(), name='review'),
    # path('anleitung-passphrase', TemplateView.as_view(template_name="users/anleitung-passphrase.html"), name='passphrase')
]
