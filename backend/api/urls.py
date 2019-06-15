from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter

from . import views


router = DefaultRouter()

seminars = router.register("seminars", views.SeminarViewSet, basename="seminar")
seminars.register(
    "comments",
    views.SeminarCommentViewSet,
    basename="seminars-comment",
    parents_query_lookups=["seminar__uuid"],
)
router.register("users", views.UserViewSet, basename="user")
router.register("groups", views.JANUNGroupViewSet, basename="janungroup")
router.register("group_names", views.JANUNGroupNamesViewSet, basename="janungroup")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_auth.urls")),
    path("auth/registration/", include("rest_auth.registration.urls")),
    path("auth/username-exists/", views.UsernameExistsView.as_view()),
    path("auth/email-exists/", views.EmailExistsView.as_view()),
]
