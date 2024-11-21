from django.core.validators import FileExtensionValidator
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from product.models import Product
from shared.models import BaseModel
from shared.validators import validate_image


class AssetType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class Asset(BaseModel):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("IN_USE", "In Use"),
        ("MAINTENANCE", "Under Maintenance"),
        ("LOST", "Lost"),
    ]

    CONDITION_CHOICES = [
        ("NEW", "New"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("POOR", "Poor"),
        ("DAMAGED", "Damaged"),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=50, unique=True, help_text="Unique identifier for the item"
    )
    type = models.ForeignKey(
        AssetType, on_delete=models.CASCADE, blank=False, null=False
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="GOOD"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="AVAILABLE"
    )

    thumbnail = models.ImageField(
        upload_to="asset_media",
        validators=[
            validate_image,
            FileExtensionValidator(["jpg", "jpeg", "png", "gif", "bmp", "webp"]),
        ],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )
    stock = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True
    )
