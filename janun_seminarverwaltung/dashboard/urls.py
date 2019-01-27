from django.urls import path

from .views import StaffDashboard, TeamerDashboard
from utils import dispatch_by_user
# from .views import Dashboard

app_name = 'dashboard'


urlpatterns = [
    path('',
        dispatch_by_user(
            verwalter_view=StaffDashboard.as_view(),
            pruefer_view=StaffDashboard.as_view(),
            teamer_view=TeamerDashboard.as_view()
        ), name='dashboard'
    )
]
