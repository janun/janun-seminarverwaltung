from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, include
from django.views.generic import TemplateView


# from rest_framework import routers
from rest_framework_extensions.routers import (
    ExtendedDefaultRouter as DefaultRouter
)

from .api import views

router = DefaultRouter()
(
    router.register('seminars', views.SeminarViewSet, base_name="seminar")
    .register(
        'comments',
        views.SeminarCommentViewSet,
        base_name="seminars-comment",
        parents_query_lookups=['seminar']
    )
)
router.register('users', views.UserViewSet, base_name="user")
router.register('groups', views.JANUNGroupViewSet, base_name="janungroup")
router.register('group_names', views.JANUNGroupNamesViewSet,
                base_name="janungroup")


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # path('manifest.json',
    #      TemplateView.as_view(template_name='manifest.json'), name='manifest'),
    # path('service-worker.js',
    #      TemplateView.as_view(template_name='service-worker.js', content_type='text/javascript'), name='worker'),

    path('api/', include(router.urls)),

    path('api/auth/login/', views.LoginView.as_view(), name='rest_login'),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    path('api/auth/username-exists/', views.UsernameExistsView.as_view()),
    path('api/auth/email-exists/', views.EmailExistsView.as_view()),

    path('api/admin/', admin.site.urls),

    re_path(r'^.*', views.index_view, name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
