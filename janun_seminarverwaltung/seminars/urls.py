from django.urls import path
from .views import SeminarListView, SeminarDetailView, SeminarWizardView

app_name = 'seminars'

seminar_wizard = SeminarWizardView.as_view(
    url_name='seminars:create_step', done_step_name='done'
)

urlpatterns = [
    path('', SeminarListView.as_view(), name='list'),
    path('<int:pk>/', SeminarDetailView.as_view(), name='detail'),
    # path('create', SeminarCreateView.as_view(), name='create'),
    path('create/<str:step>/', seminar_wizard, name='create_step'),
    path('create/', seminar_wizard, name='create'),
    # path('create/', SeminarWizardView.as_view(), name='create'),
]
