from django.urls import path

from .views import VerwalterDashboard, PrueferDashboard, TeamerDashboard
from utils import dispatch_by_user

app_name = 'dashboard'


urlpatterns = [
    path('',
         dispatch_by_user(
             VerwalterDashboard.as_view(),
             PrueferDashboard.as_view(),
             TeamerDashboard.as_view()
         ),
         name='dashboard'
        ),
]
