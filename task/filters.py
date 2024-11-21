import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    user_id = django_filters.UUIDFilter(
        field_name="warehouse_person__user", lookup_expr="exact"
    )

    class Meta:
        model = Task
        fields = ["user_id"]
