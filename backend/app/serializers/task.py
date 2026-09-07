from rest_framework import serializers

from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User

from .user import UserInfoSerializer


class TaskDetailsMeta:
    model = Task
    fields = [
        "id",
        "title",
        "description",
        "status",
        "priority",
        "creator",
        "assignee_id",
        "assignee",
        "due_date",
        'created_at',
        'updated_at',
    ]
    read_only_fields = ['id', 'created_at', 'updated_at']


class TaskCreateSerializer(serializers.ModelSerializer[Task]):
    assignee_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.filter(is_active=True),
        allow_null=True,
        required=False,
        source='assignee',
    )
    assignee = UserInfoSerializer(read_only=True, allow_null=True)

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        default='',
    )
    status = serializers.ChoiceField(
        choices=TaskStatus.choices,
        required=False,
        default=TaskStatus.TODO,
    )
    priority = serializers.ChoiceField(
        choices=TaskPriority.choices,
        required=False,
        default=TaskPriority.MEDIUM,
    )
    creator = UserInfoSerializer(read_only=True)

    class Meta(TaskDetailsMeta):
        pass


class TaskUpdateSerializer(serializers.ModelSerializer[Task]):
    creator = UserInfoSerializer(read_only=True)

    assignee_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.filter(is_active=True),
        allow_null=True,
        required=False,
        source='assignee',
    )
    assignee = UserInfoSerializer(read_only=True, allow_null=True)

    class Meta(TaskDetailsMeta):
        pass


class TaskListSerializer(serializers.ModelSerializer[Task]):
    assignee_id = serializers.UUIDField(
        read_only=True,
        allow_null=True,
        source='assignee.pk',
    )
    assignee = UserInfoSerializer(
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "priority",
            "assignee_id",
            "assignee",
            "due_date",
        ]


class TaskDetailSerializer(serializers.ModelSerializer[Task]):
    creator = UserInfoSerializer(
        read_only=True,
    )

    assignee_id = serializers.UUIDField(
        write_only=True,
        allow_null=True,
        source='assignee.pk',
    )
    assignee = UserInfoSerializer(
        read_only=True,
        allow_null=True,
    )

    class Meta(TaskDetailsMeta):
        pass
