from django.urls import path

from metrics.views import (
    DistributionFlowComparisonView,
    MonthlyDistributionFlow,
    ProductsAboutToExpireCount,
    ProductsExpiredCount,
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
    path(
        "distribution-flow-comparison/",
        DistributionFlowComparisonView.as_view(),
        name="distribution-flow-comparison",
    ),
    path(
        "products-expired-count/",
        ProductsExpiredCount.as_view(),
        name="products-expired-count",
    ),
]
