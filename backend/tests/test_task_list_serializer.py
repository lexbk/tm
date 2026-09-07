from __future__ import annotations

from rest_framework.test import APIClient

from app.models import Task


class TestTaskListEndpoint:
    """Tests for GET /tasks/ endpoint using TaskListSerializer."""

    def test_list_returns_minimal_representation(self, auth_client: APIClient, db, user):
        Task.objects.create(title='Task 1', status='TODO', priority='HIGH', creator=user)
        Task.objects.create(title='Task 2', status='DONE', priority='LOW', creator=user)
        response = auth_client.get('/api/v1/tasks/')
        assert response.status_code == 200
        data = response.json()
        assert 'count' in data
        assert 'results' in data
        for result in data['results']:
            assert set(result.keys()) == {'id', 'title', 'status', 'priority', 'assignee_id', 'assignee', 'due_date'}

    def test_list_excludes_description(self, auth_client: APIClient, db, user):
        Task.objects.create(title='Task', description='Secret info', creator=user)
        response = auth_client.get('/api/v1/tasks/')
        assert response.status_code == 200
        data = response.json()
        for result in data['results']:
            assert 'description' not in result

    def test_list_excludes_timestamps(self, auth_client: APIClient, db, user):
        Task.objects.create(title='Task', creator=user)
        response = auth_client.get('/api/v1/tasks/')
        assert response.status_code == 200
        data = response.json()
        for result in data['results']:
            assert 'created_at' not in result
            assert 'updated_at' not in result

    def test_list_excludes_creator(self, auth_client: APIClient, db, user):
        Task.objects.create(title='Task', creator=user)
        response = auth_client.get('/api/v1/tasks/')
        assert response.status_code == 200
        data = response.json()
        for result in data['results']:
            assert 'creator' not in result

    def test_list_assignee_id_is_null_when_unassigned(self, auth_client: APIClient, db, user):
        Task.objects.create(title='Unassigned Task', creator=user)
        response = auth_client.get('/api/v1/tasks/')
        assert response.status_code == 200
        data = response.json()
        for result in data['results']:
            assert result['assignee_id'] is None

    def test_list_assignee_id_includes_uuid_when_assigned(self, auth_client: APIClient, db, user, another_user):
        Task.objects.create(title='Assigned Task', creator=user, assignee=another_user)
        response = auth_client.get('/api/v1/tasks/')
        assert response.status_code == 200
        data = response.json()
        assigned_result = [r for r in data['results'] if r['title'] == 'Assigned Task'][0]
        assert assigned_result['assignee_id'] == str(another_user.pk)

    def test_list_still_supports_filtering(self, auth_client: APIClient, db, user):
        Task.objects.create(title='Todo Task', status='TODO', creator=user)
        Task.objects.create(title='Done Task', status='DONE', creator=user)
        response = auth_client.get('/api/v1/tasks/', {'status': 'TODO'})
        assert response.status_code == 200
        assert response.json()['count'] == 1

    def test_list_still_supports_ordering(self, auth_client: APIClient, db, user):
        Task.objects.create(title='First', creator=user)
        Task.objects.create(title='Second', creator=user)
        response = auth_client.get('/api/v1/tasks/', {'ordering': 'title'})
        assert response.status_code == 200
        data = response.json()
        titles = [r['title'] for r in data['results']]
        assert titles == sorted(titles)
