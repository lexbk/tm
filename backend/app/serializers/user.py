from __future__ import annotations

from rest_framework import serializers

from ..models import User


class UserInfoSerializer(serializers.Serializer[dict[str, object]]):
    id = serializers.UUIDField()
    username = serializers.CharField()


class RegisterUserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict[str, object]) -> User:
        return User.objects.create_user(**validated_data)  # type: ignore[arg-type]
