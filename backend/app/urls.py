from __future__ import annotations

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .routers import TruncatedNestedSimpleRouter
from .views.comment import CommentViewSet
from .views.task import TaskViewSet
from .views.user import UserViewSet

tasks_router = DefaultRouter()
tasks_router.register(r'tasks', TaskViewSet, basename='task')

comments_router = TruncatedNestedSimpleRouter(tasks_router, r'tasks', lookup='task_id')
comments_router.register(r'comments', CommentViewSet, basename='task-comments')

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    *tasks_router.urls,
    *comments_router.urls,
    *users_router.urls,
]
