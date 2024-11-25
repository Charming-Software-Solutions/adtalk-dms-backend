from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from shared.generic_viewset import GenericViewset
from shared.utils.s3_functions import remove_file_from_s3

from .models import Employee
from .serializers import EmployeeSerializer, UpdateEmployeeProfileSerializer


@receiver(post_delete, sender=Employee)
def employee_post_delete(sender, instance, **kwargs):
    if instance.profile_image:
        remove_file_from_s3(sender, instance, "profile_image", **kwargs)
    if instance.user:
        instance.user.delete()


class EmployeeViwset(GenericViewset):
    protected_views = "all"
    queryset = Employee.objects.all().order_by("-updated_at")
    serializer_class = EmployeeSerializer
    permissions = [IsAdminUser, IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class RetrieveOwnEmployeeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_object(self):
        try:
            return Employee.objects.get(user=self.request.user)
        except Employee.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"detail": "Employee not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateEmployeeProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateEmployeeProfileSerializer

    def get_object(self):
        return self.request.user.employee
