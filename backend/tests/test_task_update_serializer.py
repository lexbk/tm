from __future__ import annotations

from uuid import uuid4

from rest_framework import status
from rest_framework.test import APIClient

from app.models import Task


def test_update_task_full_payload(auth_client: APIClient, task):
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
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == 'Updated Title'
    assert data['description'] == 'Updated Description'
    assert data['status'] == 'DONE'
    assert data['priority'] == 'HIGH'
    refreshed = Task.objects.get(pk=task.pk)
    assert refreshed.title == 'Updated Title'
    assert refreshed.status == 'DONE'
    assert refreshed.priority == 'HIGH'


def test_patch_task_partial_payload(auth_client: APIClient, task):
    response = auth_client.patch(
        f'/api/v1/tasks/{task.pk}/',
        {'status': 'DONE'},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['status'] == 'DONE'
    refreshed = Task.objects.get(pk=task.pk)
    assert refreshed.status == 'DONE'


def test_patch_task_empty_payload_is_noop(auth_client: APIClient, task):
    original_title = task.title
    original_status = task.status
    response = auth_client.patch(
        f'/api/v1/tasks/{task.pk}/',
        {},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == original_title
    assert data['status'] == original_status
    refreshed = Task.objects.get(pk=task.pk)
    assert refreshed.title == original_title
    assert refreshed.status == original_status


def test_put_task_with_invalid_assignee(auth_client: APIClient, task):
    fake_uuid = uuid4()
    response = auth_client.put(
        f'/api/v1/tasks/{task.pk}/',
        {
            'title': 'Updated',
            'assignee_id': str(fake_uuid),
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'assignee_id' in response.json()


def test_patch_task_with_null_assignee(auth_client: APIClient, task_with_assignee):
    response = auth_client.patch(
        f'/api/v1/tasks/{task_with_assignee.pk}/',
        {'assignee_id': None},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['assignee'] is None
    refreshed = Task.objects.get(pk=task_with_assignee.pk)
    assert refreshed.assignee is None

