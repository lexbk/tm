from __future__ import annotations

from django.contrib import admin
from django.contrib.auth import get_user_model

from app.models import Comment, Task

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ['username', 'email', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ['title', 'status', 'priority', 'creator', 'assignee', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'description']
    autocomplete_fields = ['creator', 'assignee']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ['id', 'task', 'author', 'body', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['body']
    autocomplete_fields = ['task', 'author']
