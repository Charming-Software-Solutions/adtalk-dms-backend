from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from shared.generic_viewset import GenericViewset
from shared.utils.s3_functions import remove_file_from_s3

from .models import Employee
from .serializers import EmployeeSerializer


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
