from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from backend.users.views import ProfileView


urlpatterns = [
    path("", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile", ProfileView.as_view(), name="account_profile"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
