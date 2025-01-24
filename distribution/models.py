from django.db import models

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
    ba_reference_number = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="Reference number for allocations.",
    )
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, null=False, blank=False
    )
    client = models.CharField(max_length=255, null=False, blank=False)
    employee = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")

    def save(self, *args, **kwargs):
        # Track the original status
        is_new = self.pk is None
        original_status = None

        # Only try to get original status if the object is not new
        if not is_new:
            try:
                original_status = Distribution.objects.get(pk=self.pk).status
            except Distribution.DoesNotExist:
                # Fallback to None if the object can't be retrieved
                original_status = None

        super().save(*args, **kwargs)

        # Only process stock changes for existing objects with status change
        if (
            not is_new
            and original_status is not None
            and original_status != self.status
        ):
            self.process_stock_changes(original_status)

    def process_stock_changes(self, original_status):
        if self.status in ["DELIVERED", "COMPLETED"]:
            for distribution_product in self.products.all():
                product = distribution_product.product
                quantity = distribution_product.quantity

                if self.type == "EXPORT":
                    product.stock -= quantity
                elif self.type == "IMPORT":
                    product.stock += quantity

                product.save()

        # Handle stock reversal for cancelled or returned exports
        elif (
            (self.status in ["CANCELLED", "RETURNED"])
            and original_status in ["DELIVERED", "COMPLETED"]
            and self.type == "EXPORT"
        ):
            for distribution_product in self.products.all():
                product = distribution_product.product
                quantity = distribution_product.quantity

                product.stock += quantity
                product.save()

    def update_status(self, new_status):
        """
        Convenience method to update status with stock management
        """
        self.status = new_status
        self.save()


class DistributionProduct(BaseModel):
    distribution = models.ForeignKey(
        Distribution, on_delete=models.CASCADE, related_name="products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    expiration = models.DateTimeField(blank=False, null=False)


class DistributionAsset(BaseModel):
    distribution = models.ForeignKey(
        Distribution, on_delete=models.CASCADE, related_name="assets"
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
