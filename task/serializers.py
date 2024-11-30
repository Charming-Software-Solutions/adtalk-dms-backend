from rest_framework import serializers

from distribution.serializers import DistributionSerializer
from employee.models import Employee
from employee.serializers import EmployeeSerializer
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
        response["warehouse_person"] = EmployeeSerializer(
            instance.warehouse_person
        ).data
        return response
