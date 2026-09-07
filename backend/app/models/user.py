from __future__ import annotations

from uuid import UUID, uuid4

from django.contrib.auth import get_user_model as django_get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import (
    CharField,
    EmailField,
    UUIDField,
)


class User(AbstractUser):
    id: UUIDField[UUID, UUID] = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    username: CharField[str, str] = CharField(unique=True, max_length=150)
    email: EmailField[str, str] = EmailField(unique=True, db_index=True)

    objects = UserManager()

    class Meta:
        app_label = 'app'

    def __str__(self) -> str:
        return self.username


def get_user_model() -> type[User]:
    """Fix false positive IDE type checking."""

    return django_get_user_model()  # type: ignore[return-value]
