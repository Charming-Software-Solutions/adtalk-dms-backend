from django.urls import include, path
from rest_framework.routers import DefaultRouter

from product.views import (
    ProductBrandViewset,
    ProductBulkCreateView,
    ProductCategoryViewset,
    ProductTypeViewset,
    ProductViewset,
)

app_name = "product"

router = DefaultRouter()
router.register(r"brand", ProductBrandViewset, basename="brand")
router.register(r"category", ProductCategoryViewset, basename="category")
router.register(r"type", ProductTypeViewset, basename="type")
router.register(r"", ProductViewset, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("bulk-create", ProductBulkCreateView.as_view(), name="bulk-create"),
]
