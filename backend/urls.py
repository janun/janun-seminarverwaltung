from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static

from backend.users import views as user_views


urlpatterns = [
    path("", include("backend.dashboard.urls")),
    path("seminars/", include("backend.seminars.urls")),
    path("groups/", include("backend.groups.urls")),
    path("users/", include("backend.users.urls")),
    path("config/", include("backend.config.urls")),
    path("config/emails/", include("backend.emails.urls")),
    path("accounts/profile", user_views.ProfileView.as_view(), name="account_profile"),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("allauth_2fa.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    urlpatterns += [
        path("403_csrf/", TemplateView.as_view(template_name="403_csrf.html")),
        path("403/", TemplateView.as_view(template_name="403.html")),
        path("404/", TemplateView.as_view(template_name="404.html")),
        path("500/", TemplateView.as_view(template_name="500.html")),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
