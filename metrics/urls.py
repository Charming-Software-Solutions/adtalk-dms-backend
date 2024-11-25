from django.urls import path

from metrics.views import (
    MonthlyDistributionFlow,
    ProductsAboutToExpireCount,
    RemainingTaskCount,
    TotalItemStock,
)

app_name = "metrics"

urlpatterns = [
    path("total-item-stock/", TotalItemStock.as_view(), name="total-item-stock"),
    path(
        "monthly-distribution-flow/",
        MonthlyDistributionFlow.as_view(),
        name="monthly-distribution-flow",
    ),
    path(
        "remaining-task-count/",
        RemainingTaskCount.as_view(),
        name="weekly-remaining-task-count/",
    ),
    path(
        "products-about-to-expire-count/",
        ProductsAboutToExpireCount.as_view(),
        name="products-about-to-expire-count",
    ),
]
