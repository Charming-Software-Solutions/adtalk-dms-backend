from rest_framework import serializers

from distribution.serializers import DistributionSerializer
from employee.models import Employee
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    warehouse_person = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )  # Use PK relation here

    class Meta:
        model = Task
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["distribution"] = DistributionSerializer(instance.distribution).data
        # Serializing warehouse_person to include id and name in the response
        if instance.warehouse_person:
            response["warehouse_person"] = {
                "user": instance.warehouse_person.user.id,
                "id": instance.warehouse_person.id,
                "name": instance.warehouse_person.name,
            }
        return response
