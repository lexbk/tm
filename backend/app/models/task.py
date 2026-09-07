from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from django.db.models import (
    PROTECT,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    Model,
    TextChoices,
    TextField,
    UUIDField,
)


class TaskStatus(TextChoices):
    TODO = 'TODO', 'To Do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    DONE = 'DONE', 'Done'


class TaskPriority(TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    URGENT = 'URGENT', 'Urgent'


class Task(Model):
    id: UUIDField[str, str] = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    title: CharField[str, str] = CharField(max_length=255)
    description: TextField[str, str] = TextField(blank=True, default='')
    status: CharField[str, str] = CharField(
        max_length=len(TaskStatus.IN_PROGRESS),
        choices=TaskStatus,
        default=TaskStatus.TODO,
    )
    priority: CharField[str, str] = CharField(
        max_length=len(TaskPriority.URGENT),
        choices=TaskPriority,
        default=TaskPriority.MEDIUM,
    )
    creator: ForeignKey['Task', 'Task'] = ForeignKey(
        'app.User',
        on_delete=PROTECT,
        related_name='created_tasks',
    )
    assignee: ForeignKey['Task', 'Task'] = ForeignKey(
        'app.User',
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
    )
    due_date: DateTimeField[datetime, datetime] = DateTimeField(null=True, blank=True)
    created_at: DateTimeField[datetime, datetime] = DateTimeField(auto_now_add=True)
    updated_at: DateTimeField[datetime, datetime] = DateTimeField(auto_now=True)

    class Meta:
        app_label = 'app'
        indexes = [
            Index(fields=['status']),
            Index(fields=['priority']),
            Index(fields=['creator']),
            Index(fields=['assignee']),
            Index(fields=['due_date']),
            Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return self.title
