from django.urls import path
from .views import (SeminarListView, SeminarDetailView, SeminarWizardView,
                    SeminarDeleteView, SeminarChangeStateView, SeminarEditView,
                    SeminarCommentCreateView, SeminarCommentDeleteView)

app_name = 'seminars'

seminar_wizard = SeminarWizardView.as_view(
    url_name='seminars:create_step', done_step_name='done'
)

urlpatterns = [
    path('', SeminarListView.as_view(), name='list'),
    path('<int:pk>/', SeminarDetailView.as_view(), name='detail'),
    path('<int:pk>/state/<str:transition>', SeminarChangeStateView.as_view(), name='change_state'),
    path('create/<str:step>/', seminar_wizard, name='create_step'),
    path('create/', seminar_wizard, name='create'),
    path('<int:pk>/delete', SeminarDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit', SeminarEditView.as_view(), name='edit'),
    path('<int:pk>/comment', SeminarCommentCreateView.as_view(), name='create_comment'),
    path('<int:seminar_pk>/delete_comment/<int:pk>', SeminarCommentDeleteView.as_view(), name='delete_comment'),
]
