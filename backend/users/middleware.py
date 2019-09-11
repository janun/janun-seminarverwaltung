from django.utils import timezone
from .models import User


class SetLastVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # update last_visit without updating auto_add fields
            User.objects.filter(pk=request.user.pk).update(last_visit=timezone.now())
        return response
