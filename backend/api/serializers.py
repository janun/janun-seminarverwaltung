from typing import Dict

from django.contrib.auth.hashers import make_password
from django.db.models import Model, QuerySet
from django.http import HttpRequest
from rest_auth.registration.serializers import (
    RegisterSerializer as OldRegisterSerializer,
)
from rest_framework import serializers

from . import models


class ChoicesField(serializers.Field):
    def __init__(self, choices: Dict[str, str], **kwargs) -> None:
        self._choices = choices
        super().__init__(**kwargs)

    def to_representation(self, value) -> str:
        return self._choices[value]

    def to_internal_value(self, data) -> str:
        return getattr(self._choices, data)


# Short Serializers
# ------------------------------------------------------------------------------


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("pk", "username", "name")


class ShortJANUNGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JANUNGroup
        fields = ("pk", "name")


# Full Serializers
# ------------------------------------------------------------------------------


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer used by user administration

    UserProfileSerializer inherits from this one
    """

    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    janun_groups = ShortJANUNGroupSerializer(read_only=True, many=True)
    janun_groups_pks = serializers.PrimaryKeyRelatedField(
        queryset=models.JANUNGroup.objects.all(), many=True, source="janun_groups"
    )
    group_hats = ShortJANUNGroupSerializer(read_only=True, many=True)
    group_hats_pks = serializers.PrimaryKeyRelatedField(
        queryset=models.JANUNGroup.objects.all(), many=True, source="group_hats"
    )

    password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )

    @staticmethod
    def setup_eager_loading(queryset: QuerySet) -> QuerySet:
        "add prefetch related to the queryset for performance"
        queryset = queryset.prefetch_related("janun_groups", "group_hats")
        return queryset

    def create(self, validated_data: Dict[str, str]) -> Dict[str, str]:
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance: Model, validated_data: Dict[str, str]) -> models.User:
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)

    class Meta:
        model = models.User
        fields = (
            "pk",
            "username",
            "name",
            "janun_groups",
            "janun_groups_pks",
            "group_hats",
            "group_hats_pks",
            "role",
            "telephone",
            "address",
            "created_at",
            "updated_at",
            "last_visit",
            "email",
            "password",
            "is_reviewed",
            "has_staff_role",
            "has_verwalter_role",
        )


class SeminarCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    owner = ShortUserSerializer(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset: QuerySet) -> QuerySet:
        "add prefetch related to the queryset for performance"
        queryset = queryset.select_related("owner")
        return queryset

    class Meta:
        model = models.SeminarComment
        fields = ("pk", "text", "seminar", "owner", "created_at")


class JANUNGroupSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    members = ShortUserSerializer(read_only=True, many=True)
    group_hats = ShortUserSerializer(read_only=True, many=True)

    @staticmethod
    def setup_eager_loading(queryset: QuerySet) -> QuerySet:
        "add prefetch related to the queryset for performance"
        queryset = queryset.prefetch_related("members", "group_hats")
        return queryset

    class Meta:
        model = models.JANUNGroup
        fields = ("pk", "name", "created_at", "updated_at", "members", "group_hats")


class SeminarSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    owner = ShortUserSerializer(read_only=True)
    owner_pk = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all(),
        source="owner",
        write_only=True,
        required=False,
        allow_null=True,
    )
    group = ShortJANUNGroupSerializer(read_only=True)
    group_pk = serializers.PrimaryKeyRelatedField(
        queryset=models.JANUNGroup.objects.all(),
        source="group",
        write_only=True,
        required=False,
        allow_null=True,
    )

    status = ChoicesField(choices=models.Seminar.STATES, default="angemeldet")

    @staticmethod
    def setup_eager_loading(queryset: QuerySet) -> QuerySet:
        "add prefetch related to the queryset for performance"
        queryset = queryset.select_related("owner", "group")
        return queryset

    def to_internal_value(self, data):
        "allow for optional start_time and end_time (workaround for time validation)"
        if data.get("start_time", None) == "":
            data.pop("start_time")
        if data.get("end_time", None) == "":
            data.pop("end_time")
        return super().to_internal_value(data)

    class Meta:
        model = models.Seminar
        fields = (
            "pk",
            "title",
            "status",
            "owner",
            "owner_pk",
            "group",
            "group_pk",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "location",
            "created_at",
            "updated_at",
            "description",
            "planned_training_days",
            "planned_attendees_min",
            "planned_attendees_max",
            "requested_funding",
            "tnt",
            "tnt_cost",
            "deadline",
            "deadline_expired",
            "deadline_in_two_weeks",
        )


# User Authentication and Signup Serializers
# ------------------------------------------------------------------------------


class UserProfileSerializer(UserSerializer):
    """
    Serializer used for self viewing and editing each user profile
    So permission fields need to be read_only here
    """

    janun_groups_pks = serializers.PrimaryKeyRelatedField(
        many=True, source="janun_groups", read_only=True
    )
    group_hats_pks = serializers.PrimaryKeyRelatedField(
        many=True, source="group_hats", read_only=True
    )

    class Meta(UserSerializer.Meta):
        read_only_fields = ("is_reviewed", "role")


class RegisterSerializer(OldRegisterSerializer):
    """
    Serializer used for new user signup
    """

    username = serializers.CharField(min_length=3, required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(write_only=True)
    telephone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    janun_groups_pks = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=models.JANUNGroup.objects.all()
    )

    def custom_signup(self, request: HttpRequest, user: models.User) -> None:
        user.name = self.validated_data.get("name", "")
        user.telephone = self.validated_data.get("telephone", "")
        user.address = self.validated_data.get("address", "")
        user.janun_groups.set(self.validated_data.get("janun_groups_pks", []))
        user.save()
