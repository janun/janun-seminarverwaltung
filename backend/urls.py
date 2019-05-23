from django.conf import settings
from django.urls import include, path, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path("api/", include("backend.api.urls")),
    re_path(r"^.*", TemplateView.as_view(template_name="index.html")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
