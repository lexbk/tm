from __future__ import annotations

from uuid import uuid4

from rest_framework.test import APIClient

from app.models import Task


class TestTaskUpdateEndpoint:
    """Tests for PUT /tasks/{pk}/ and PATCH /tasks/{pk}/ endpoints."""

    def test_update_task_full_payload(self, auth_client: APIClient, task):
        response = auth_client.put(
            f'/api/v1/tasks/{task.pk}/',
            {
                'title': 'Updated Title',
                'description': 'Updated Description',
                'status': 'DONE',
                'priority': 'HIGH',
            },
            format='json',
        )
        assert response.status_code == 200
        data = response.json()
        assert data['title'] == 'Updated Title'
        assert data['description'] == 'Updated Description'
        assert data['status'] == 'DONE'
        assert data['priority'] == 'HIGH'
        refreshed = Task.objects.get(pk=task.pk)
        assert refreshed.title == 'Updated Title'
        assert refreshed.status == 'DONE'
        assert refreshed.priority == 'HIGH'

    def test_patch_task_partial_payload(self, auth_client: APIClient, task):
        response = auth_client.patch(
            f'/api/v1/tasks/{task.pk}/',
            {'status': 'DONE'},
            format='json',
        )
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'DONE'
        refreshed = Task.objects.get(pk=task.pk)
        assert refreshed.status == 'DONE'

    def test_patch_task_with_assignee(self, auth_client: APIClient, task, another_user):
        response = auth_client.patch(
            f'/api/v1/tasks/{task.pk}/',
            {'assignee_id': str(another_user.pk)},
            format='json',
        )
        assert response.status_code == 200
        data = response.json()
        assert data['assignee']['id'] == str(another_user.pk)

    def test_patch_task_empty_payload_is_noop(self, auth_client: APIClient, task):
        original_title = task.title
        original_status = task.status
        response = auth_client.patch(
            f'/api/v1/tasks/{task.pk}/',
            {},
            format='json',
        )
        assert response.status_code == 200
        data = response.json()
        assert data['title'] == original_title
        assert data['status'] == original_status
        refreshed = Task.objects.get(pk=task.pk)
        assert refreshed.title == original_title
        assert refreshed.status == original_status

    def test_patch_task_creator_is_ignored(self, auth_client: APIClient, task, another_user):
        original_creator_pk = task.creator.pk
        response = auth_client.patch(
            f'/api/v1/tasks/{task.pk}/',
            {'creator_id': str(another_user.pk)},
            format='json',
        )
        assert response.status_code == 200
        data = response.json()
        assert data['creator']['id'] == str(original_creator_pk)
        refreshed = Task.objects.get(pk=task.pk)
        assert refreshed.creator.pk == original_creator_pk

    def test_put_task_with_invalid_assignee(self, auth_client: APIClient, task):
        fake_uuid = uuid4()
        response = auth_client.put(
            f'/api/v1/tasks/{task.pk}/',
            {
                'title': 'Updated',
                'assignee_id': str(fake_uuid),
            },
            format='json',
        )
        assert response.status_code == 400
        assert 'assignee_id' in response.json()

    def test_patch_task_with_null_assignee(self, auth_client: APIClient, task_with_assignee):
        response = auth_client.patch(
            f'/api/v1/tasks/{task_with_assignee.pk}/',
            {'assignee_id': None},
            format='json',
        )
        assert response.status_code == 200
        data = response.json()
        assert data['assignee'] is None
        refreshed = Task.objects.get(pk=task_with_assignee.pk)
        assert refreshed.assignee is None

    def test_patch_task_preserves_creator(self, auth_client: APIClient, task):
        original_creator_pk = task.creator.pk
        response = auth_client.patch(
            f'/api/v1/tasks/{task.pk}/',
            {'title': 'Updated'},
            format='json',
        )
        assert response.status_code == 200
        refreshed = Task.objects.get(pk=task.pk)
        assert refreshed.creator.pk == original_creator_pk
