from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from rest_framework import serializers


def _make_mixin(auto_set_fields: dict[str, str]):
    """Create a minimal serializer class with the mixin for testing."""
    from app.serializers.common import AutoCreatorMixin

    return type(
        'TestSerializer',
        (AutoCreatorMixin, serializers.ModelSerializer),
        {
            'auto_set_fields': auto_set_fields,
            'Meta': type('Meta', (), {'model': None, 'fields': ['title']}),
        },
    )


def test_sets_creator_from_authenticated_user():
    user = MagicMock()
    type(user).is_anonymous = PropertyMock(return_value=False)

    mock_request = MagicMock()
    mock_request.user = user

    TestSerializer = _make_mixin({'creator': 'creator'})
    serializer = TestSerializer(context={'request': mock_request})

    validated_data: dict = {'title': 'test'}
    try:
        serializer.create(validated_data)
    except AttributeError:
        pass

    assert 'creator' in validated_data
    assert validated_data['creator'] == user


def test_sets_author_from_authenticated_user():
    user = MagicMock()
    type(user).is_anonymous = PropertyMock(return_value=False)

    mock_request = MagicMock()
    mock_request.user = user

    TestSerializer = _make_mixin({'author': 'author'})
    serializer = TestSerializer(context={'request': mock_request})

    validated_data: dict = {'body': 'test'}
    try:
        serializer.create(validated_data)
    except AttributeError:
        pass

    assert 'author' in validated_data
    assert validated_data['author'] == user


def test_is_noop_for_anonymous_user():
    mock_request = MagicMock()
    type(mock_request.user).is_anonymous = PropertyMock(return_value=True)

    TestSerializer = _make_mixin({'creator': 'creator'})
    serializer = TestSerializer(context={'request': mock_request})

    validated_data: dict = {'title': 'test'}
    try:
        serializer.create(validated_data)
    except AttributeError:
        pass

    assert 'creator' not in validated_data
