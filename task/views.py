from django.shortcuts import render

from shared.generic_viewset import GenericViewset
from task.models import Task
from task.serializers import TaskSerializer


class TaskViewset(GenericViewset):
    include_list_view = True
    protected_views = ["create", "update", "partial_update", "destroy"]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer