from __future__ import annotations

from rest_framework.test import APIClient

from app.models import Task


class TestTaskDetailEndpoint:
    """Tests for GET /tasks/{pk}/ endpoint using TaskDetailSerializer."""

    def test_retrieve_returns_full_representation(self, auth_client: APIClient, db, user):
        task = Task.objects.create(
            title='Full Task',
            description='Full task description',
            status='IN_PROGRESS',
            priority='HIGH',
            creator=user,
        )
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/')
        assert response.status_code == 200
        data = response.json()
        assert set(data.keys()) == {
            'id',
            'title',
            'description',
            'status',
            'priority',
            'creator',
            'assignee',
            'due_date',
            'created_at',
            'updated_at',
        }

    def test_retrieve_includes_creator(self, auth_client: APIClient, db, user):
        task = Task.objects.create(title='Task', creator=user)
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/')
        assert response.status_code == 200
        data = response.json()
        assert data['creator'] is not None
        assert 'id' in data['creator']
        assert 'username' in data['creator']

    def test_retrieve_assignee_is_null_when_unassigned(
        self, auth_client: APIClient, db, user
    ):
        task = Task.objects.create(title='Unassigned', creator=user)
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/')
        assert response.status_code == 200
        data = response.json()
        assert data['assignee'] is None

    def test_retrieve_assignee_includes_user_info_when_assigned(
        self, auth_client: APIClient, db, user, another_user
    ):
        task = Task.objects.create(
            title='Assigned', creator=user, assignee=another_user
        )
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/')
        assert response.status_code == 200
        data = response.json()
        assert data['assignee'] is not None
        assert data['assignee']['id'] == str(another_user.pk)
        assert 'username' in data['assignee']

    def test_retrieve_includes_timestamps(self, auth_client: APIClient, db, user):
        task = Task.objects.create(title='Task', creator=user)
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/')
        assert response.status_code == 200
        data = response.json()
        assert 'created_at' in data
        assert 'updated_at' in data
        assert 'due_date' in data
