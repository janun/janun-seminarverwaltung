from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.mixins import NestedViewSetMixin

from . import models
from . import permissions as permissions2
from . import serializers
from . import filters


class SeminarViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    "Seminars"
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SeminarSerializer
    lookup_field = "uuid"
    filterset_class = filters.SeminarFilter

    def get_queryset(self) -> QuerySet:
        if self.request.user.has_staff_role:
            # staff members can access any seminar
            qs = models.Seminar.objects.all()
        else:
            # teamers can only access their own seminars
            qs = self.request.user.seminars
        qs = self.get_serializer_class().setup_eager_loading(qs)  # type: ignore
        return qs

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)


class SeminarCommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    "Comments on Seminars"
    permission_classes = (permissions2.IsOwnerOrVerwalterOrReadOnly,)
    queryset = models.SeminarComment.objects.all()
    serializer_class = serializers.SeminarCommentSerializer
    lookup_field = "uuid"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        qs = self.get_serializer_class().setup_eager_loading(qs)  # type: ignore
        return qs

    def perform_create(self, serializer) -> None:
        seminar = models.Seminar.objects.get(
            uuid=self.kwargs["parent_lookup_seminar__uuid"]
        )
        serializer.save(owner=self.request.user, seminar=seminar)


class JANUNGroupViewSet(viewsets.ModelViewSet):
    "Groups"
    permission_classes = (
        permissions.IsAuthenticated,
        permissions2.HasVerwalterRoleOrReadOnly,
        permissions2.IsReviewed,
    )
    serializer_class = serializers.JANUNGroupSerializer
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet:
        if self.request.user.has_staff_role:
            # staff members can access any group
            qs = models.JANUNGroup.objects.all()
        else:
            # teamers can only access their own groups
            qs = self.request.user.janun_groups
        qs = self.get_serializer_class().setup_eager_loading(qs)  # type: ignore
        return qs


class UserViewSet(viewsets.ModelViewSet):
    "Users"
    permission_classes = (
        permissions2.HasStaffRole,
        permissions2.HasVerwalterRoleOrReadOnly,
    )
    serializer_class = serializers.UserSerializer
    lookup_field = "username"
    filterset_class = filters.UserFilter

    def get_queryset(self) -> QuerySet:
        qs = models.User.objects.all()
        qs = self.get_serializer_class().setup_eager_loading(qs)  # type: ignore
        return qs


# Public viewsets
# ------------------------------------------------------------------------------


class JANUNGroupNamesViewSet(viewsets.ModelViewSet):
    """
    Return a list all existing JANUNGroups (name and slug only)
    (Used as a data source for select form elements)
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ShortJANUNGroupSerializer
    queryset = models.JANUNGroup.objects.all()


class UsernameExistsView(APIView):
    """
    Checks if username exists in database
    (Helper for signup views)
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request: HttpRequest) -> HttpResponse:
        username = request.GET.get("username", "").strip().lower()
        exists = models.User.objects.filter(username=username).exists()
        return Response({"exists": exists}, content_type="application/json")


class EmailExistsView(APIView):
    """
    Checks if email address exists in database
    (Helper for signup views)
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request: HttpRequest) -> HttpResponse:
        email = request.GET.get("email", "").strip().lower()
        exists = models.User.objects.filter(email=email).exists()
        return Response({"exists": exists}, content_type="application/json")
