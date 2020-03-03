from django.urls import path

from . import views

app_name = "seminars"

urlpatterns = [
    path("", views.SeminarListView.as_view(), name="list"),
    path(
        "calc_max_funding", views.CalcMaxFundingView.as_view(), name="calc_max_funding"
    ),
    path("import", views.SeminarImportView.as_view(), name="import"),
    path("<int:year>", views.StaffSeminarListView.as_view(), name="list_staff"),
    path("all", views.StaffSeminarListView.as_view(), name="list_staff_all"),
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
    path(
        "<int:year>/<slug:slug>/apply_done",
        views.SeminarApplyDoneView.as_view(),
        name="apply_done",
    ),
    # edit:
    path("<int:year>/<slug:slug>", views.SeminarUpdateView.as_view(), name="detail"),
    path(
        "<int:year>/<slug:slug>/history",
        views.SeminarHistoryView.as_view(),
        name="history",
    ),
    path(
        "<int:year>/<slug:slug>/teamer",
        views.SeminarTeamerUpdateView.as_view(),
        name="detail_teamer",
    ),
    path(
        "<int:year>/<slug:slug>/staff",
        views.SeminarStaffUpdateView.as_view(),
        name="detail_staff",
    ),
    # delete:
    path(
        "<int:year>/<slug:slug>/delete",
        views.SeminarDeleteView.as_view(),
        name="delete",
    ),
    # create:
    path("apply", views.SeminarApplyView.as_view(), name="apply"),
    # comments:
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
