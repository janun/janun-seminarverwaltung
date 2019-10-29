from django.urls import path
from django.conf import settings

from . import views

app_name = "seminars"

urlpatterns = [
    path("", views.SeminarView.as_view(), name="list"),
    # path("import", views.SeminarImportView.as_view(), name="import"),
    path("<int:year>", views.StaffSeminarListView.as_view(), name="list_staff"),
    path("<int:year>/export", views.SeminarExportView.as_view(), name="export"),
    path(
        "<int:year>/funding_rates",
        views.FundingRateUpdateView.as_view(),
        name="funding_rates",
    ),
    path(
        "<int:year>/proof_of_use",
        views.SeminarProofOfUseView.as_view(),
        name="proof_of_use",
    ),
    path("your", views.YourSeminarListView.as_view(), name="list_yours"),
    path("<int:year>/<slug:slug>", views.SeminarUpdateView.as_view(), name="detail"),
    path(
        "<int:year>/<slug:slug>/delete",
        views.SeminarDeleteView.as_view(),
        name="delete",
    ),
    path("apply", views.SeminarApplyView.as_view(), name="apply"),
    path(
        "<int:year>/<slug:slug>/comments",
        views.CommentListView.as_view(),
        name="comment_list",
    ),
    path(
        "<int:year>/<slug:slug>/comments/create",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "comments/<int:pk>/delete",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]

if settings.DEBUG:
    urlpatterns += [path("apply_done_test", views.SeminarApplyDoneTestView.as_view())]
