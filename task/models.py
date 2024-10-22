from django.db import models

from distribution.models import Distribution
from shared.models import BaseModel


class Task(BaseModel):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("RECEIVED", "Received"),
        ("CHECKED_IN", "Checked In"),
        ("STOCKED", "Stocked"),
        ("SHELVED", "Shelved"),
        ("PICKED", "Picked"),
        ("PACKED", "Packed"),
        ("LOADED", "Loaded"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
    )

    employee = models.CharField(max_length=255, null=False, blank=False)
    distribution = models.ForeignKey(
        Distribution, on_delete=models.CASCADE, related_name="tasks"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")
