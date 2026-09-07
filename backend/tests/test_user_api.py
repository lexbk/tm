from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


def test_unauthenticated_returns_401(db, client: APIClient):
    response = client.get('/api/v1/users/')
    assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


def test_list_returns_paginated_results(db, auth_client: APIClient, user, another_user):
    response = auth_client.get('/api/v1/users/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'count' in data
    assert 'next' in data
    assert 'previous' in data
    assert 'results' in data
    assert isinstance(data['results'], list)
    assert len(data['results']) == 2

    first = data['results'][0]
    assert 'id' in first
    assert 'username' in first


def test_inactive_users_excluded(db, auth_client: APIClient, user, another_user):
    User.objects.filter(pk=another_user.pk).update(is_active=False)
    response = auth_client.get('/api/v1/users/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    usernames = [u['username'] for u in data['results']]
    assert another_user.username not in usernames
    assert user.username in usernames
