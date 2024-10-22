from rest_framework import serializers

from distribution.serializers import DistributionSerializer
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["distribution"] = DistributionSerializer(instance.distribution).data
        return response
