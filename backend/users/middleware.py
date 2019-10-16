import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User


class SetLastVisitMiddleware:
    """Updates last_visit field on currently logged in user in each request"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # update last_visit without updating auto_add fields
            User.objects.filter(pk=request.user.pk).update(last_visit=timezone.now())
        return response


class RequireLoginMiddleware:
    """
    Required Login everywhere

    Except for url listed in setting LOGIN_REQUIRED_URLS_EXCEPTIONS

    For example:
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/account/login(.*)$',
        r'/account/logout(.*)$',
    )
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.exceptions = tuple(
            re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS
        )

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            return None

        for url in self.exceptions:
            if url.match(request.path):
                return None

        return login_required(view_func)(request, *view_args, **view_kwargs)
