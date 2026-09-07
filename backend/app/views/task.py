from __future__ import annotations

from typing import Any

from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.filters import OrderingFilter

from ..models import Task
from ..serializers.task import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
    TaskUpdateSerializer,
)
from .filters import TaskFilter


@extend_schema_view(
    list=extend_schema(
        summary="List tasks",
        description="Return a paginated list of tasks.",
        responses=TaskListSerializer(many=True),
    ),
    retrieve=extend_schema(
        summary="Get task",
        description="Return detailed information about a task.",
        responses=TaskDetailSerializer,
    ),
    create=extend_schema(
        summary="Create task",
        description="Create a new task.",
        # request=TaskCreateSerializer,
        responses=TaskCreateSerializer,
        # responses=TaskDetailSerializer,
    ),
    update=extend_schema(
        summary="Update task",
        description="Replace an existing task.",
        request=TaskUpdateSerializer,
        responses=TaskDetailSerializer,
    ),
    partial_update=extend_schema(
        summary="Partially update task",
        description="Update selected fields of an existing task.",
        request=TaskUpdateSerializer,
        responses=TaskDetailSerializer,
    ),
    destroy=extend_schema(
        summary="Delete task",
        description="Delete an existing task.",
        responses=None,
    ),
)
class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet[Any],
):
    """API endpoints for managing tasks.

    Tasks belong to a creator and may optionally be assigned
    to another user.
    """

    queryset = Task.objects.select_related('creator', 'assignee')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']

    _serializers = {
        "list": TaskListSerializer,
        "retrieve": TaskDetailSerializer,
        "create": TaskCreateSerializer,
        "update": TaskUpdateSerializer,
        "partial_update": TaskUpdateSerializer,
    }

    def get_serializer_class(self) -> type[serializers.BaseSerializer[Any]]:
        return self._serializers.get(self.action, TaskDetailSerializer)

    def perform_create(self, serializer: serializers.BaseSerializer[Any]) -> None:
        serializer.save(creator=self.request.user)
