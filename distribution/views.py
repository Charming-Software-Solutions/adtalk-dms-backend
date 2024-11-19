from typing import Any, Dict, List
from uuid import UUID

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import generics

from distribution.models import Distribution
from distribution.serializers import DistributionSerializer
from product.models import Product
from shared.generic_viewset import GenericViewset
from shared.permissions import IsLogisticsOrAdmin


class DistributionViewset(GenericViewset):
    include_list_view = True
    protected_views = ["create", "update", "partial_update", "destroy"]
    queryset = Distribution.objects.all().order_by("-updated_at")
    serializer_class = DistributionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsLogisticsOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class DistributionCheckProductsView(generics.GenericAPIView):
    def is_valid_product(self, product_id: str) -> bool:
        try:
            UUID(product_id)
            return Product.objects.filter(id=product_id).exists()
        except ValueError:
            return False

    def post(self, request: Request) -> Response:
        products: List[Dict[str, Any]] = request.data.get("products", [])

        if not products:
            return Response({"valid": False, "message": "No products provided."})

        all_products_valid = all(
            self.is_valid_product(item.get("product", "")) for item in products
        )

        return Response({"valid": all_products_valid})
