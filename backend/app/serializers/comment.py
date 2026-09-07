from __future__ import annotations

from rest_framework import serializers

from ..models import Comment
from .common import AutoCreatorMixin
from .user import UserInfoSerializer


class CommentCreateSerializer(AutoCreatorMixin, serializers.ModelSerializer[Comment]):
    author = UserInfoSerializer(read_only=True)

    body = serializers.CharField(
        required=True,
        max_length=10000,
    )

    auto_set_fields: dict[str, str] = {'author': 'author'}

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_body(self, value: str) -> str:
        if not value or not value.strip():
            raise serializers.ValidationError('Body must not be empty or whitespace-only.')
        return value


class CommentUpdateSerializer(serializers.ModelSerializer[Comment]):
    author = UserInfoSerializer(read_only=True)

    body = serializers.CharField(
        required=True,
        max_length=10000,
    )

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_body(self, value: str) -> str:
        if not value or not value.strip():
            raise serializers.ValidationError('Body must not be empty or whitespace-only.')
        return value


class CommentListSerializer(serializers.ModelSerializer[Comment]):
    author = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'created_at', 'updated_at']


class CommentDetailSerializer(serializers.ModelSerializer[Comment]):
    author = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'created_at', 'updated_at']
        read_only_fields = fields
