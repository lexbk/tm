from __future__ import annotations

from django.db import models

from app.models import Task


def get_task_queryset() -> models.QuerySet[Task]:
    return Task.objects.select_related('creator', 'assignee')
