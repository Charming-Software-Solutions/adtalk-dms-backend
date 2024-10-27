from django.core.validators import FileExtensionValidator
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from shared.models import BaseModel
from shared.validators import validate_image


class ProductBrand(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)


class ProductCategory(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)


class ProductType(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)


class Product(BaseModel):
    sku = models.CharField(max_length=50, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    brand = models.ForeignKey(
        ProductBrand, on_delete=models.CASCADE, blank=False, null=False
    )
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, blank=False, null=False
    )
    type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, blank=False, null=False
    )
    thumbnail = models.ImageField(
        upload_to="product_media",
        validators=[
            validate_image,
            FileExtensionValidator(["jpg", "jpeg", "png", "gif", "bmp", "webp"]),
        ],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )
    stock = models.PositiveIntegerField(default=0)
    flavor = models.CharField(max_length=255, blank=True, null=True)
