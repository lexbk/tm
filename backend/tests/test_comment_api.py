from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from uuid import uuid4

from app.models import Comment

User = get_user_model()


class TestCommentListCreate:
    def test_unauthenticated_returns_401(self, db, client: APIClient, task):
        response = client.get(f'/api/v1/tasks/{task.pk}/comments/')
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_list_returns_empty_for_task_with_no_comments(self, auth_client: APIClient, task):
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/comments/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'count' in data
        assert 'results' in data
        assert data['count'] == 0
        assert data['results'] == []

    def test_list_returns_comments_for_task(self, auth_client: APIClient, task, another_user):
        comment1 = Comment.objects.create(task=task, body='First comment', author=another_user)
        comment2 = Comment.objects.create(task=task, body='Second comment', author=task.creator)
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/comments/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['count'] == 2
        assert len(data['results']) == 2

    def test_list_comments_only_for_specified_task(self, auth_client: APIClient, task, task_with_assignee, another_user):
        Comment.objects.create(task=task, body='Comment for task 1', author=another_user)
        Comment.objects.create(task=task_with_assignee, body='Comment for task 2', author=another_user)
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/comments/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['count'] == 1
        assert data['results'][0]['body'] == 'Comment for task 1'

    def test_create_comment(self, auth_client: APIClient, task):
        response = auth_client.post(
            f'/api/v1/tasks/{task.pk}/comments/',
            {'body': 'This is a test comment'},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['body'] == 'This is a test comment'
        assert data['author'] is not None
        assert data['author']['id'] == str(task.creator.pk)
        assert data['author']['username'] == 'testuser'
        assert Comment.objects.filter(task=task, body='This is a test comment').exists()

    def test_create_comment_with_whitespace_body_returns_400(self, auth_client: APIClient, task):
        response = auth_client.post(
            f'/api/v1/tasks/{task.pk}/comments/',
            {'body': '   '},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_comment_with_empty_body_returns_400(self, auth_client: APIClient, task):
        response = auth_client.post(
            f'/api/v1/tasks/{task.pk}/comments/',
            {'body': ''},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_comment_with_body_exceeding_max_length_returns_400(self, auth_client: APIClient, task):
        body = 'x' * 10001
        response = auth_client.post(
            f'/api/v1/tasks/{task.pk}/comments/',
            {'body': body},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_comment_with_body_at_max_length_succeeds(self, auth_client: APIClient, task):
        body = 'x' * 10000
        response = auth_client.post(
            f'/api/v1/tasks/{task.pk}/comments/',
            {'body': body},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_comment_author_is_set_from_request_user(self, auth_client: APIClient, task, another_user):
        response = auth_client.post(
            f'/api/v1/tasks/{task.pk}/comments/',
            {'body': 'Comment by another user'},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['author']['id'] == str(task.creator.pk)
        assert data['author']['username'] == 'testuser'
        # Even if client sends author, it should be ignored
        response2 = auth_client.post(
            f'/api/v1/tasks/{task.pk}/comments/',
            {'body': 'Another comment', 'author': str(another_user.pk)},
            format='json',
        )
        assert response2.status_code == status.HTTP_201_CREATED
        data2 = response2.json()
        assert data2['author']['id'] == str(task.creator.pk)


class TestCommentDetail:
    def test_retrieve_comment(self, auth_client: APIClient, task):
        comment = Comment.objects.create(task=task, body='Some comment', author=task.creator)
        response = auth_client.get(f'/api/v1/tasks/{task.pk}/comments/{comment.pk}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == str(comment.pk)
        assert data['body'] == 'Some comment'
        assert data['author'] is not None
        assert 'id' in data['author']
        assert 'username' in data['author']

    def test_retrieve_comment_for_nonexistent_task_returns_404(self, auth_client: APIClient):
        response = auth_client.get(f'/api/v1/tasks/{uuid4()}/comments/{uuid4()}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_comment(self, auth_client: APIClient, task):
        comment = Comment.objects.create(task=task, body='Original body', author=task.creator)
        response = auth_client.patch(
            f'/api/v1/tasks/{task.pk}/comments/{comment.pk}/',
            {'body': 'Updated body'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['body'] == 'Updated body'
        refreshed = Comment.objects.get(pk=comment.pk)
        assert refreshed.body == 'Updated body'

    def test_patch_any_user_can_update_any_comment(self, auth_client: APIClient, task, another_user):
        comment = Comment.objects.create(task=task, body='Original body', author=another_user)
        response = auth_client.patch(
            f'/api/v1/tasks/{task.pk}/comments/{comment.pk}/',
            {'body': 'Updated by another user'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['body'] == 'Updated by another user'
        refreshed = Comment.objects.get(pk=comment.pk)
        assert refreshed.body == 'Updated by another user'

    def test_delete_comment(self, auth_client: APIClient, task):
        comment = Comment.objects.create(task=task, body='To delete', author=task.creator)
        response = auth_client.delete(f'/api/v1/tasks/{task.pk}/comments/{comment.pk}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(pk=comment.pk).exists()

    def test_delete_nonexistent_comment(self, auth_client: APIClient, task):
        response = auth_client.delete(f'/api/v1/tasks/{task.pk}/comments/{uuid4()}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_any_user_can_delete_any_comment(self, auth_client: APIClient, task, another_user):
        comment = Comment.objects.create(task=task, body='Another user comment', author=another_user)
        response = auth_client.delete(f'/api/v1/tasks/{task.pk}/comments/{comment.pk}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(pk=comment.pk).exists()


class TestCommentTaskCascade:
    def test_deleting_task_deletes_comments(self, db, task):
        Comment.objects.create(task=task, body='Comment 1', author=task.creator)
        Comment.objects.create(task=task, body='Comment 2', author=task.creator)
        task_pk = task.pk
        task.delete()
        assert not Comment.objects.filter(pk__in=Comment.objects.filter(task_id=task_pk)).exists()


class TestCommentUserSetNull:
    def test_deleting_user_sets_author_to_null(self, db, task, another_user):
        comment = Comment.objects.create(task=task, body='Orphan comment', author=another_user)
        another_user.delete()
        refreshed = Comment.objects.get(pk=comment.pk)
        assert refreshed.author is None
        assert refreshed.body == 'Orphan comment'
