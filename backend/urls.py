from django.conf import settings
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path("", include("backend.dashboard.urls")),
    path("seminars/", include("backend.seminars.urls")),
    path("groups/", include("backend.groups.urls")),
    path("accounts/", include("backend.users.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
