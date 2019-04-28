from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer as OldRegisterSerializer
from rest_auth import serializers as rest_auth_serializers
from django.contrib.auth.hashers import make_password


from . import models


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super().__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'pk', 'username', 'name',
        )


class ShortJANUNGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.JANUNGroup
        fields = (
            'pk', 'name'
        )


class UserSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    janun_groups = ShortJANUNGroupSerializer(read_only=True, many=True)
    group_hats = ShortJANUNGroupSerializer(read_only=True, many=True)

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('janun_groups', 'group_hats')
        return queryset

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = models.User
        fields = (
            'pk', 'username', 'name', 'janun_groups', 'group_hats', 'role',
            'telephone', 'address', 'created_at', 'updated_at', 'email', 'password', 'is_reviewed'
        )


class SeminarCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    owner = ShortUserSerializer(read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        return queryset

    class Meta:
        model = models.SeminarComment
        fields = (
            'pk', 'text', 'seminar', 'owner', 'created_at'
        )


class JANUNGroupSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    members = ShortUserSerializer(read_only=True, many=True)
    group_hats = ShortUserSerializer(read_only=True, many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('members', 'group_hats')
        return queryset

    class Meta:
        model = models.JANUNGroup
        fields = (
            'pk', 'name', 'created_at', 'updated_at', 'members', 'group_hats'
        )


class SeminarSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    owner = ShortUserSerializer(read_only=True)
    group = ShortJANUNGroupSerializer(read_only=True)
    # group = serializers.SlugRelatedField(
    #     slug_field="name", queryset=models.JANUNGroup.objects.all(),
    #     allow_null=True
    # )

    status = ChoicesField(choices=models.Seminar.STATES, default="angemeldet")

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner', 'group')
        return queryset

    def to_internal_value(self, data):
        if data.get('start_time', None) == '':
            data.pop('start_time')
        if data.get('end_time', None) == '':
            data.pop('end_time')
        return super().to_internal_value(data)

    class Meta:
        model = models.Seminar
        fields = (
            'pk', 'title', 'status', 'owner', 'group',
            'start_date', 'start_time', 'end_date', 'end_time',
            'location', 'created_at', 'updated_at',
            'description',
            'planned_training_days',
            'planned_attendees_min',
            'planned_attendees_max',
            'requested_funding',
            'tnt',
            'tnt_cost',
            'deadline'
        )


class RegisterSerializer(OldRegisterSerializer):
    name = serializers.CharField(write_only=True)
    password2 = None
    telephone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    # TODO: janun_groups

    def validate(self, data):
        return data

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.telephone = self.validated_data.get('telephone', '')
        user.address = self.validated_data.get('address', '')
        user.save()

    def validate_password(self, password):
        return get_adapter().clean_password(password)


class LoginResponseSerializer(serializers.Serializer):
    token = rest_auth_serializers.TokenSerializer()
    user = UserSerializer()
