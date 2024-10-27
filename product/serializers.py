from rest_framework import serializers

from .models import Product, ProductBrand, ProductCategory, ProductType


class ProductBulkCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        product_data = [Product(**item) for item in validated_data]
        return Product.objects.bulk_create(product_data)


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(required=False, write_only=False)
    list_serializer_class = ProductBulkCreateSerializer

    class Meta:
        model = Product
        fields = "__all__"

    def update(self, instance, validated_data):
        # Thubnail
        thumbnail = validated_data.pop("thumbnail", None)
        if thumbnail is not None:
            instance.thumbnail = thumbnail

        # Update all other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["brand"] = ProductBrandSerializer(instance.brand).data
        response["category"] = ProductCategorySerializer(instance.category).data
        response["type"] = ProductTypeSerializer(instance.type).data
        return response
