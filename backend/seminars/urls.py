from django.urls import path
from . import views

urlpatterns = [
    path("", views.SeminarListView.as_view(), name="seminar_list"),
    path(
        "<int:year>/<slug:slug>",
        views.SeminarUpdateView.as_view(),
        name="seminar_detail",
    ),
    path("apply", views.SeminarApplyView.as_view(), name="seminar_apply"),
    path(
        "comments/<int:pk>/delete",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
