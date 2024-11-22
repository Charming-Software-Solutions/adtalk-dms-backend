from datetime import timedelta

from django.db.models import Count, F, Sum
from django.utils import timezone
from rest_framework import permissions, views
from rest_framework.request import Request
from rest_framework.response import Response

from asset.models import Asset
from distribution.models import Distribution
from product.models import Product
from task.models import Task


class TotalItemStock(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        total_asset_stock = Asset.objects.aggregate(total_asset_stock=Sum("stock")).get(
            "total_asset_stock", 0
        )
        total_product_stock = Product.objects.aggregate(
            total_product_stock=Sum("stock")
        ).get("total_product_stock", 0)

        total_item_stock = total_asset_stock + total_product_stock
        return Response({"value": total_item_stock})


class MonthlyDistributionFlow(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        current_date = timezone.now()

        total_distributions = Distribution.objects.filter(
            status="COMPLETED",
            created_at__year=current_date.year,
            created_at__month=current_date.month,
        ).count()

        return Response({"value": total_distributions})


class WeeklyRemainingTaskCount(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        current_date = timezone.now()
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(
            days=6, hours=23, minutes=59, seconds=59
        )

        remaining_tasks = (
            Task.objects.exclude(status__in=["DELIVERED", "SHELVED"])
            .filter(created_at__range=(start_of_week, end_of_week))
            .count()
        )

        return Response({"value": remaining_tasks})


class ProductsAboutToExpireCount(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        current_date = timezone.now()
        one_month_from_now = current_date + timedelta(days=30)

        products_about_to_expire = Product.objects.filter(
            expiration__gte=current_date,
            expiration__lte=one_month_from_now,
        ).count()

        return Response({"value": products_about_to_expire})
