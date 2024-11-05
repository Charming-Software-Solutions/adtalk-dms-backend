from django.db.models.signals import pre_delete
from django.dispatch import receiver
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from product.models import Product, ProductBrand, ProductCategory, ProductType
from product.serializers import (
    ProductBrandSerializer,
    ProductCategorySerializer,
    ProductSerializer,
    ProductTypeSerializer,
)
from shared.generic_viewset import GenericViewset
from shared.utils.s3_functions import remove_file_from_s3


@receiver(pre_delete, sender=Product)
def product_pre_delete(sender, instance, **kwargs):
    remove_file_from_s3(sender, instance, "thumbnail", **kwargs)


class ProductBrandViewset(GenericViewset):
    protected_views = ["create", "update", "partial_update", "destroy"]
    queryset = ProductBrand.objects.all().order_by("-updated_at")
    serializer_class = ProductBrandSerializer


class ProductCategoryViewset(GenericViewset):
    protected_views = ["create", "update", "partial_update", "destroy"]
    queryset = ProductCategory.objects.all().order_by("-updated_at")
    serializer_class = ProductCategorySerializer


class ProductTypeViewset(GenericViewset):
    protected_views = ["create", "update", "partial_update", "destroy"]
    queryset = ProductType.objects.all().order_by("-updated_at")
    serializer_class = ProductTypeSerializer


class ProductViewset(GenericViewset):
    protected_views = ["create", "update", "partial_update", "destroy"]
    queryset = Product.objects.all().order_by("-updated_at")
    serializer_class = ProductSerializer


class ProductBulkCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)
