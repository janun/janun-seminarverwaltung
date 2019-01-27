from django.urls import path
from utils import dispatch_by_user
from . import views

app_name = 'seminars'

seminar_wizard = views.SeminarWizardView.as_view(
    url_name='seminars:create_step', done_step_name='done'
)

urlpatterns = [
    path('', dispatch_by_user(
        verwalter_view=views.SeminarStaffListView.as_view(),
        pruefer_view=views.SeminarStaffListView.as_view(),
        teamer_view=views.SeminarTeamerListView.as_view()
        ), name='list'
    ),
    path('<int:pk>/', views.SeminarDetailView.as_view(), name='detail'),
    path('<int:pk>/state/<str:transition>', views.SeminarChangeStateView.as_view(), name='change_state'),
    path('create/<str:step>/', seminar_wizard, name='create_step'),
    path('create/', seminar_wizard, name='create'),
    path('<int:pk>/delete', views.SeminarDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit', views.SeminarEditView.as_view(), name='edit'),
    path('<int:pk>/comment', views.SeminarCommentCreateView.as_view(), name='create_comment'),
    path('<int:seminar_pk>/delete_comment/<int:pk>', views.SeminarCommentDeleteView.as_view(), name='delete_comment'),
]
