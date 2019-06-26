from django.conf import settings
from django.urls import include, path, re_path
from django.views.generic import TemplateView


urlpatterns = [path("", include("backend.api.urls"))]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
