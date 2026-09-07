from __future__ import annotations

from uuid import uuid4

from rest_framework.test import APIClient

from app.models import Task


def test_creates_task_with_valid_payload(auth_client: APIClient, db):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'New Task',
            'description': 'Task Description',
            'priority': 'HIGH',
            'status': 'TODO',
        },
        format='json',
    )
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'New Task'
    assert data['description'] == 'Task Description'
    assert data['priority'] == 'HIGH'
    assert data['status'] == 'TODO'
    assert 'id' in data
    assert 'creator' in data
    assert 'created_at' in data
    assert Task.objects.filter(title='New Task').exists()


def test_creates_task_with_minimal_payload(auth_client: APIClient, db):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Minimal Task',
        },
        format='json',
    )
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'Minimal Task'
    assert data['description'] == ''
    assert data['status'] == 'TODO'
    assert data['priority'] == 'MEDIUM'


def test_returns_400_when_title_missing(auth_client: APIClient, db):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'description': 'No title',
        },
        format='json',
    )
    assert response.status_code == 400
    assert 'title' in response.json()


def test_returns_400_with_invalid_assignee_uuid(auth_client: APIClient, db):
    fake_uuid = uuid4()
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Bad Task',
            'assignee_id': str(fake_uuid),
        },
        format='json',
    )
    assert response.status_code == 400
    assert 'assignee_id' in response.json()


def test_returns_400_with_nonexistent_assignee_uuid(auth_client: APIClient, db):
    fake_uuid = uuid4()
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Bad Task',
            'assignee_id': str(fake_uuid),
        },
        format='json',
    )
    assert response.status_code == 400


def test_creates_task_with_valid_assignee(auth_client: APIClient, db, another_user):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Assigned Task',
            'assignee_id': str(another_user.pk),
        },
        format='json',
    )
    assert response.status_code == 201
    data = response.json()
    assert data['assignee'] is not None
    assert data['assignee']['id'] == str(another_user.pk)


def test_creates_task_with_null_assignee(auth_client: APIClient, db):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Unassigned Task',
            'assignee_id': None,
        },
        format='json',
    )
    assert response.status_code == 201
    data = response.json()
    assert data['assignee'] is None


def test_sets_creator_from_authenticated_user(auth_client: APIClient, db):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Creator Task',
        },
        format='json',
    )
    assert response.status_code == 201
    data = response.json()
    assert data['creator'] is not None
    assert 'id' in data['creator']
    assert 'username' in data['creator']
