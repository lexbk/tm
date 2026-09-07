from __future__ import annotations

from datetime import datetime

from django.db import models
from django.utils import timezone
from django_filters import rest_framework as filters

from ..models import Task
from ..models.task import TaskPriority, TaskStatus


class DateOrDateTimeFilter(filters.Filter):
    """Filter that supports both date and datetime inputs on a DateTimeField.

    Accepts `?due_date=2025-01-15` or `?due_date=2025-01-15T10:30:00Z`.
    """

    def filter(self, qs: models.QuerySet[Task], value: str) -> models.QuerySet[Task]:
        if value:
            try:
                dt = timezone.make_aware(datetime.fromisoformat(value))
                return qs.filter(**{self.field_name: dt})
            except (ValueError, TypeError, AttributeError):
                return qs.filter(**{f'{self.field_name}__date': value})
        return qs


class TaskFilter(filters.FilterSet):
    """FilterSet for Task with explicit filter declarations.

    Uses ChoiceFilter for status/priority (respects TextChoices).
    Uses CharFilter with __pk lookup for creator (handles UUID strings).
    Uses custom DateOrDateTimeFilter for due_date (handles date and datetime inputs).
    """

    status = filters.ChoiceFilter(choices=TaskStatus)
    priority = filters.ChoiceFilter(choices=TaskPriority)
    creator = filters.CharFilter(field_name='creator__pk')
    assignee_id = filters.CharFilter(field_name='assignee__pk')
    due_date = DateOrDateTimeFilter(field_name='due_date')

    class Meta:
        model = Task
        fields: list[str] = []
