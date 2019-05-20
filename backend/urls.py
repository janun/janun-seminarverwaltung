from django.conf import settings
from django.urls import include, path, re_path
from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter

from .api import views


router = DefaultRouter()

seminars = router.register("seminars", views.SeminarViewSet, basename="seminar")
seminars.register(
    "comments",
    views.SeminarCommentViewSet,
    basename="seminars-comment",
    parents_query_lookups=["seminar"],
)
router.register("users", views.UserViewSet, basename="user")
router.register("groups", views.JANUNGroupViewSet, basename="janungroup")
router.register("group_names", views.JANUNGroupNamesViewSet, basename="janungroup")


urlpatterns = [
    path("", views.index_view, name="index"),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_auth.urls")),
    path("api/auth/registration/", include("rest_auth.registration.urls")),
    path("api/auth/username-exists/", views.UsernameExistsView.as_view()),
    path("api/auth/email-exists/", views.EmailExistsView.as_view()),
    re_path(r"^.*", views.index_view, name="index"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
