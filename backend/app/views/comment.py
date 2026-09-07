from __future__ import annotations

from typing import Any

from django.db import models
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.exceptions import NotFound

from ..models import Comment, Task
from ..serializers.comment import (
    CommentCreateSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
    CommentUpdateSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List comments",
        description="Return a paginated list of comments for a task.",
        responses=CommentListSerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Get comment",
        description="Return detailed information about a comment.",
        responses=CommentDetailSerializer,
    ),
    create=extend_schema(
        summary="Create comment",
        description="Create a new comment on a task.",
        responses=CommentCreateSerializer,
    ),
    update=extend_schema(
        summary="Update comment",
        description="Replace an existing comment.",
        request=CommentUpdateSerializer,
        responses=CommentDetailSerializer,
    ),
    partial_update=extend_schema(
        summary="Partially update comment",
        description="Update selected fields of an existing comment.",
        request=CommentUpdateSerializer,
        responses=CommentDetailSerializer,
    ),
    destroy=extend_schema(
        summary="Delete comment",
        description="Delete an existing comment.",
        responses=None,
    ),
)
class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet[Any],
):
    _serializers = {
        "list": CommentListSerializer,
        "retrieve": CommentDetailSerializer,
        "create": CommentCreateSerializer,
        "update": CommentUpdateSerializer,
        "partial_update": CommentUpdateSerializer,
    }

    permission_classes = [permissions.IsAuthenticated]

    @property
    def task_id(self) -> str | None:
        return self.kwargs.get('task_id')

    def get_serializer_class(self) -> type[serializers.BaseSerializer[Any]]:
        return self._serializers.get(self.action, CommentDetailSerializer)

    def get_queryset(self) -> models.QuerySet[Comment]:
        if not self.task_id:
            return Comment.objects.none()
        try:
            task = Task.objects.get(pk=self.task_id)
        except (Task.DoesNotExist, ValueError) as e:
            raise NotFound('Task not found.') from e
        return Comment.objects.filter(task=task).select_related('author')

    def perform_create(self, serializer: serializers.BaseSerializer[Any]) -> None:
        task = Task.objects.get(pk=self.task_id)
        serializer.save(task=task)
