from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User

from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    Model,
    UUIDField,
)


class Comment(Model):
    id: UUIDField[str, str] = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    task: ForeignKey['Task', 'Task'] = ForeignKey(
        'app.Task',
        on_delete=CASCADE,
        related_name='comments',
    )
    author: ForeignKey['User', 'User'] = ForeignKey(
        'app.User',
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='comments',
    )
    body: CharField[str, str] = CharField(max_length=10000)
    created_at: DateTimeField[datetime, datetime] = DateTimeField(auto_now_add=True)
    updated_at: DateTimeField[datetime, datetime] = DateTimeField(auto_now=True)

    class Meta:
        app_label = 'app'
        indexes = [
            Index(fields=['task']),
        ]

    def __str__(self) -> str:
        return f'Comment by {self.author} on {self.task}'
