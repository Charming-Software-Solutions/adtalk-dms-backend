from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from shared.generic_viewset import GenericViewset
from task.models import Task
from task.serializers import TaskSerializer


class TaskViewset(GenericViewset):
    include_list_view = True
    protected_views = ["create", "update", "partial_update", "destroy"]
    queryset = Task.objects.all().order_by("-updated_at")
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
