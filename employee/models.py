from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from shared.models import BaseModel
from shared.validators import validate_image


class Employee(BaseModel):
    first_name = models.CharField(max_length=100, blank=False, null=False, unique=False)
    last_name = models.CharField(max_length=100, blank=False, null=False, unique=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
    )
    profile_image = models.ImageField(
        upload_to="employee_media",
        validators=[
            validate_image,
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
        ],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )
