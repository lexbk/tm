from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from ..serializers.user import RegisterUserSerializer, UserInfoSerializer

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description="Return a paginated list of active users.",
        responses=UserInfoSerializer(many=True),
    ),
)
class UserViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet[Any],
):
    """API endpoint for listing active users."""

    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer


# REGISTER
@api_view(['POST'])
def register(request: Request) -> Response:
    serializer: RegisterUserSerializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "User created"})
    return Response(serializer.errors)
