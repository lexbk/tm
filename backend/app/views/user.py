from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from ..serializers.user import RegisterUserSerializer

User = get_user_model()


# REGISTER
@api_view(['POST'])
def register(request: Request) -> Response:
    serializer: RegisterUserSerializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "User created"})
    return Response(serializer.errors)
