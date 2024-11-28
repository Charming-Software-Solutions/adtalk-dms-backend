from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import permissions, views
from rest_framework.request import Request
from rest_framework.response import Response

from asset.models import Asset
from distribution.models import Distribution
from product.models import Product
from task.models import Task


def get_daily_metric(
    model,
    status_field: str,
    status_value: str,
    date_field: str,
    date: datetime,
    aggregate_field: Optional[str] = None,
    count: bool = False,
) -> Decimal | int:
    filter_params = {
        status_field: status_value,
        f"{date_field}__date": date,
    }

    if count:
        return (
            model.objects.filter(**filter_params).aggregate(total=Count("id"))["total"]
            or 0
        )
    elif aggregate_field:
        return model.objects.filter(**filter_params).aggregate(
            total=Sum(aggregate_field)
        )["total"] or Decimal("0.00")
    else:
        raise ValueError(
            "Either 'aggregate_field' must be provided or 'count' must be True."
        )


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


class RemainingTaskCount(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        remaining_tasks = Task.objects.exclude(
            status__in=["DELIVERED", "SHELVED"]
        ).count()

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


class DistributionFlowComparisonView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        current_date = timezone.now()
        start_date = current_date - timedelta(days=30)
        end_date = current_date

        data = []

        date = start_date
        while date <= end_date:
            export_count = get_daily_metric(
                model=Distribution,
                status_field="type",
                status_value="EXPORT",
                date_field="created_at",
                date=date,
                count=True,
            )
            import_count = get_daily_metric(
                model=Distribution,
                status_field="type",
                status_value="IMPORT",
                date_field="created_at",
                date=date,
                count=True,
            )

            data.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "export": export_count,
                    "import": import_count,
                }
            )

            date += timedelta(days=1)

        return Response(data)
