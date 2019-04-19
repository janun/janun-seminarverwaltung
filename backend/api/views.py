from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework_extensions.mixins import DetailSerializerMixin
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.etag.mixins import ETAGMixin


from rest_auth import views as rest_auth_views

from . import models, serializers, filters
from . import permissions as permissions2


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class SeminarViewSet(NestedViewSetMixin, ETAGMixin, CacheResponseMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SeminarSerializer
    filterset_class = filters.SeminarFilter

    def get_queryset(self):
        if self.request.user.role in ("Prüfer_in", "Verwalter_in"):
            qs = models.Seminar.objects.all()
        else:
            qs = self.request.user.seminars
        qs = self.get_serializer_class().setup_eager_loading(qs)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SeminarCommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions2.IsOwnerOrReadOnly,)
    queryset = models.SeminarComment.objects.all()
    serializer_class = serializers.SeminarCommentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self.get_serializer_class().setup_eager_loading(qs)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JANUNGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.JANUNGroupSerializer

    def get_queryset(self):
        if self.request.user.role in ("Prüfer_in", "Verwalter_in"):
            qs = models.JANUNGroup.objects.all()
        else:
            qs = self.request.user.janun_groups
        qs = self.get_serializer_class().setup_eager_loading(qs)
        return qs


class JANUNGroupNamesViewSet(viewsets.ViewSet):
    """Helper for signup views"""
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        groups = [group.name for group in models.JANUNGroup.objects.all()]
        return Response(groups)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserSerializer
    filter_fields = ('janun_groups', 'group_hats')

    def get_queryset(self):
        if self.request.user.role in ("Prüfer_in", "Verwalter_in"):
            qs = models.User.objects.all()
        else:
            qs = self.request.user
        qs = self.get_serializer_class().setup_eager_loading(qs)
        return qs


# class UserExistsViewSet(viewsets.ViewSet):
#     """Helper for signup views"""
#     permission_classes = (permissions.AllowAny,)

class UsernameExistsView(APIView):
    """Helper for signup views"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        username = request.GET.get('username', '').strip().lower()
        exists = models.User.objects.filter(username=username).exists()
        return Response({'exists': exists}, content_type="application/json")


class EmailExistsView(APIView):
    """Helper for signup views"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        email = request.GET.get('email', '').strip().lower()
        exists = models.User.objects.filter(email=email).exists()
        return Response({'exists': exists}, content_type="application/json")


class LoginView(rest_auth_views.LoginView):
    """customized LoginView to also return user object on login"""

    def get_response_serializer(self):
        return serializers.LoginResponseSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()
        data = {
            'user': self.user,
            'token': {'key': self.token}
        }
        serializer = serializer_class(instance=data, context={
                                      'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
