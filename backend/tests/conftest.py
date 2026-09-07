from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from app.models import Task

User = get_user_model()


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def clean_db(db) -> None:
    User.objects.filter(username__in=['user1', 'user2']).delete()


@pytest.fixture
def user(db, clean_db) -> User:
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
    )


@pytest.fixture
def another_user(db, clean_db) -> User:
    return User.objects.create_user(
        username='anotheruser',
        password='anotherpass123',
        email='another@example.com',
    )


@pytest.fixture
def task(db, user) -> Task:
    return Task.objects.create(
        title='Test Task',
        description='Test Description',
        creator=user,
    )


@pytest.fixture
def task_with_assignee(db, user, another_user) -> Task:
    return Task.objects.create(
        title='Assigned Task',
        description='Task with assignee',
        creator=user,
        assignee=another_user,
    )


@pytest.fixture
def auth_token(db, user, client: APIClient) -> str:
    response = client.post(
        '/api/v1/auth/token/',
        {'username': 'testuser', 'password': 'testpass123'},
        format='json',
    )
    return response.json()['access']


@pytest.fixture
def auth_client(db, auth_token: str, client: APIClient) -> APIClient:
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    return client
