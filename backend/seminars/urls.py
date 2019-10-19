from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.SeminarListView.as_view(), name="seminar_list"),
    path(
        "<int:year>/<slug:slug>",
        views.SeminarUpdateView.as_view(),
        name="seminar_detail",
    ),
    path(
        "<int:year>/<slug:slug>/delete",
        views.SeminarDeleteView.as_view(),
        name="seminar_delete",
    ),
    path("apply", views.SeminarApplyView.as_view(), name="seminar_apply"),
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
