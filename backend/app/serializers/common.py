from __future__ import annotations

from typing import Any

from django.apps import apps
from django.conf import settings
from rest_framework import serializers

from app.models.task import Task
from app.models.user import User


class AutoCreatorMixin:
    """Automatically sets creator/author from request.user on create.

    Configure per-serializer via ``auto_set_fields``:

    .. code-block:: python

        auto_set_fields = {'creator': 'creator'}  # Task
        auto_set_fields = {'author': 'author'}    # Comment

    Handles anonymous users and missing request context gracefully (no-op).
    """

    auto_set_fields: dict[str, str] = {}
    context: dict[str, Any]

    def create(self, validated_data: dict[str, Any]) -> Any:
        request = self.context.get('request')
        if request and hasattr(request, 'user') and not request.user.is_anonymous:
            for dest_field in self.auto_set_fields.values():
                validated_data[dest_field] = request.user
        return super().create(validated_data)  # type: ignore[misc]


class TaskOutputMixin(serializers.ModelSerializer[Task]):
    """Shared read-only output logic for Task serializers.

    Subclasses that want the ``assignee_info`` dict or ``creator`` UUID
    string can declare the corresponding field and rely on these methods.
    """

    def get_assignee_info(self, obj: Task) -> dict[str, str] | None:
        if obj.assignee is None:
            return None
        return {
            'id': str(obj.assignee.pk),
            'username': obj.assignee.username,  # type: ignore[attr-defined]
        }

    def get_creator_id(self, obj: Task) -> str:
        return str(obj.creator.pk)

    class Meta:
        model = Task
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskWriteSerializer(TaskOutputMixin):
    """Base for serializers that accept ``assignee`` as input.

    Adds a write-only ``assignee`` field and ``validate_assignee()``
    on top of ``TaskOutputMixin``.  Declares ``assignee_info`` and
    ``creator`` output fields so subclasses that inherit from this
    class automatically get them.
    """

    assignee = serializers.CharField(
        allow_null=True,
        required=False,
        write_only=True,
    )

    assignee_info = serializers.SerializerMethodField()
    creator_id = serializers.SerializerMethodField()

    def validate_assignee(self, value: Any) -> User | None:
        if value is None:
            return None
        from uuid import UUID

        try:
            user_id = UUID(str(value))
        except (ValueError, TypeError) as e:
            raise serializers.ValidationError('Invalid UUID format.') from e
        try:
            user_model = getattr(settings, 'AUTH_USER_MODEL', 'app.User')
            app_label = user_model.split('.')[0]
            user_model_class = apps.get_model(app_label, user_model.split('.')[1])
            if user_model_class:
                return user_model_class.objects.get(pk=user_id)
            return User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            raise serializers.ValidationError('User does not exist.') from e

    class Meta(TaskOutputMixin.Meta):
        pass
