from django.db import models
from django.utils.crypto import get_random_string

from asset.models import Asset
from product.models import Product
from shared.models import BaseModel


class Distribution(BaseModel):
    TYPE_CHOICES = (("EXPORT", "Export"), ("IMPORT", "Import"))
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_TRANSIT", "In Transit"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
        ("RETURNED", "Returned"),
        ("ON_HOLD", "On Hold"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("SCHEDULED", "Scheduled"),
    )

    dist_id = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, null=False, blank=False
    )
    client = models.CharField(max_length=255, null=False, blank=False)
    employee = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")

    def save(self, *args, **kwargs):
        if not self.dist_id:
            self.dist_id = get_random_string(length=6).upper()
        super().save(*args, **kwargs)


class DistributionProduct(BaseModel):
    distribution = models.ForeignKey(
        Distribution, on_delete=models.CASCADE, related_name="products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class DistributionAsset(BaseModel):
    distribution = models.ForeignKey(
        Distribution, on_delete=models.CASCADE, related_name="assets"
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
