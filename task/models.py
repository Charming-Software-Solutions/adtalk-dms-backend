from django.db import models

from distribution.models import Distribution
from employee.models import Employee
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

    warehouse_person = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    distribution = models.ForeignKey(
        Distribution, on_delete=models.CASCADE, related_name="tasks"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PENDING")

    class Meta:
        unique_together = ("warehouse_person", "distribution")
