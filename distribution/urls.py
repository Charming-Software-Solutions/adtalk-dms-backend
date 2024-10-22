from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DistributionCheckProductsView, DistributionViewset

app_name = "distribution"

router = DefaultRouter()
router.register(r"", DistributionViewset, basename="distribution")

urlpatterns = [
    path(
        "check-products/",
        DistributionCheckProductsView.as_view(),
        name="check-products",
    ),
    path("", include(router.urls)),
]
