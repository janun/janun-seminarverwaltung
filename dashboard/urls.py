from django.urls import path
from . import views

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),
    path("seminars/", views.SeminarListView.as_view(), name="seminar_list"),
    path(
        "seminars/<int:year>/<slug:slug>",
        views.SeminarUpdateView.as_view(),
        name="seminar_detail",
    ),
    path("seminars/apply", views.SeminarApplyView.as_view(), name="seminar_apply"),
    path(
        "comments/<int:pk>/delete",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path(
        "groups/<slug:slug>", views.JANUNGroupDetailView.as_view(), name="group_detail"
    ),
]
