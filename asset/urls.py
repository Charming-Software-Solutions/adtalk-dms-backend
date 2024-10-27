from django.urls import include, path
from rest_framework.routers import DefaultRouter

from asset.views import AssetTypeViewset, AssetViewset

app_name = "asset"

router = DefaultRouter()
router.register(r"type", AssetTypeViewset, basename="type")
router.register(r"", AssetViewset, basename="asset")

urlpatterns = [
    path("", include(router.urls)),
]
