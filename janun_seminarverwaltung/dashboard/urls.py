from django.urls import path

# from .views import VerwalterDashboard, PrueferDashboard, TeamerDashboard
# from utils import dispatch_by_user
from .views import Dashboard

app_name = 'dashboard'


urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard')
]
