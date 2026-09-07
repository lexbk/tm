from __future__ import annotations

from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from app.models import Task

User = get_user_model()


def test_unauthenticated_returns_401(db, client: APIClient):
    response = client.get('/api/v1/tasks/')
    assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


def test_list_returns_paginated_results(auth_client: APIClient):
    Task.objects.create(title='Task 1', creator=User.objects.get(username='testuser'))
    Task.objects.create(title='Task 2', creator=User.objects.get(username='testuser'))
    response = auth_client.get('/api/v1/tasks/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'count' in data
    assert 'next' in data
    assert 'previous' in data
    assert 'results' in data
    assert isinstance(data['results'], list)
    assert len(data['results']) == 2


def test_list_with_filtering_by_status(auth_client: APIClient):
    creator = User.objects.get(username='testuser')
    Task.objects.create(title='Todo Task', status='TODO', creator=creator)
    Task.objects.create(title='Done Task', status='DONE', creator=creator)
    response = auth_client.get('/api/v1/tasks/', {'status': 'TODO'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 1


def test_list_with_filtering_by_priority(auth_client: APIClient):
    creator = User.objects.get(username='testuser')
    Task.objects.create(title='Low Task', priority='LOW', creator=creator)
    Task.objects.create(title='High Task', priority='HIGH', creator=creator)
    response = auth_client.get('/api/v1/tasks/', {'priority': 'HIGH'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 1


def test_list_with_filtering_by_creator(auth_client: APIClient, another_user):
    creator = User.objects.get(username='testuser')
    Task.objects.create(title='My Task', creator=creator)
    Task.objects.create(title='Other Task', creator=another_user)
    response = auth_client.get('/api/v1/tasks/', {'creator': str(creator.pk)})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 1


def test_list_with_filtering_by_assignee(auth_client: APIClient, task_with_assignee):
    assignee = User.objects.get(username='anotheruser')
    response = auth_client.get('/api/v1/tasks/', {'assignee_id': str(assignee.pk)})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 1


def test_list_with_ordering(auth_client: APIClient):
    creator = User.objects.get(username='testuser')
    Task.objects.create(title='First', creator=creator)
    Task.objects.create(title='Second', creator=creator)
    response = auth_client.get('/api/v1/tasks/', {'ordering': 'created_at'})
    assert response.status_code == status.HTTP_200_OK


def test_list_with_descending_ordering(auth_client: APIClient):
    creator = User.objects.get(username='testuser')
    Task.objects.create(title='First', creator=creator)
    Task.objects.create(title='Second', creator=creator)
    response = auth_client.get('/api/v1/tasks/', {'ordering': '-created_at'})
    assert response.status_code == status.HTTP_200_OK


def test_create_task(auth_client: APIClient):
    creator = User.objects.get(username='testuser')
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'New Task',
            'description': 'New Task Description',
            'priority': 'HIGH',
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == 'New Task'
    assert data['description'] == 'New Task Description'
    assert data['creator'] is not None
    assert data['creator']['id'] == str(creator.pk)
    assert Task.objects.get(pk=data['id']).creator.pk == creator.pk


def test_create_task_with_assignee(auth_client: APIClient, another_user):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Assigned Task',
            'assignee_id': str(another_user.pk),
        },
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['assignee'] is not None
    assert data['assignee']['id'] == str(another_user.pk)


def test_create_task_with_invalid_assignee(auth_client: APIClient):
    response = auth_client.post(
        '/api/v1/tasks/',
        {
            'title': 'Bad Task',
            'assignee_id': str(uuid4()),
        },
        format='json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_retrieve_task(auth_client: APIClient, task):
    response = auth_client.get(f'/api/v1/tasks/{task.pk}/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == str(task.pk)
    assert data['title'] == 'Test Task'
    assert data['creator'] is not None
    assert 'id' in data['creator']
    assert 'username' in data['creator']


def test_retrieve_task_with_assignee(auth_client: APIClient, task_with_assignee):
    response = auth_client.get(f'/api/v1/tasks/{task_with_assignee.pk}/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['assignee'] is not None
    assert data['assignee']['id'] == str(task_with_assignee.assignee.pk)


def test_retrieve_task_null_assignee(auth_client: APIClient, task):
    response = auth_client.get(f'/api/v1/tasks/{task.pk}/')
    data = response.json()
    assert data['assignee'] is None


def test_retrieve_nonexistent_task(auth_client: APIClient):
    response = auth_client.get(f'/api/v1/tasks/{uuid4()}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_task(auth_client: APIClient, task):
    response = auth_client.patch(
        f'/api/v1/tasks/{task.pk}/',
        {'status': 'DONE', 'priority': 'HIGH'},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['status'] == 'DONE'
    assert data['priority'] == 'HIGH'
    refreshed = Task.objects.get(pk=task.pk)
    assert refreshed.status == 'DONE'
    assert refreshed.priority == 'HIGH'


def test_patch_task_with_assignee(auth_client: APIClient, task, another_user):
    response = auth_client.patch(
        f'/api/v1/tasks/{task.pk}/',
        {'assignee_id': str(another_user.pk)},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['assignee']['id'] == str(another_user.pk)


def test_patch_creator_is_readonly(auth_client: APIClient, task, another_user):
    response = auth_client.patch(
        f'/api/v1/tasks/{task.pk}/',
        {'creator_id': str(another_user.pk)},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['creator']['id'] == str(task.creator.pk)
    refreshed = Task.objects.get(pk=task.pk)
    assert refreshed.creator.pk == task.creator.pk


def test_delete_task(auth_client: APIClient, task):
    response = auth_client.delete(f'/api/v1/tasks/{task.pk}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(pk=task.pk).exists()


def test_delete_nonexistent_task(auth_client: APIClient):
    response = auth_client.delete(f'/api/v1/tasks/{uuid4()}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_any_user_can_manage_any_task(auth_client: APIClient, task, another_user):
    response = auth_client.delete(f'/api/v1/tasks/{task.pk}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
