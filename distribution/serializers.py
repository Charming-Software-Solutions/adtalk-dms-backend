from rest_framework import serializers

from asset.models import Asset
from asset.serializers import AssetSerializer
from distribution.models import Distribution, DistributionAsset, DistributionProduct
from product.models import Product
from product.serializers import ProductSerializer


class DistributionProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = DistributionProduct
        fields = ["product", "quantity", "expiration"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product"] = ProductSerializer(instance.product).data
        return representation


class DistributionAssetSerializer(serializers.ModelSerializer):
    asset = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all())

    class Meta:
        model = DistributionAsset
        fields = ["asset", "quantity"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["asset"] = AssetSerializer(instance.asset).data
        return representation


class DistributionSerializer(serializers.ModelSerializer):
    products = DistributionProductSerializer(many=True)
    assets = DistributionAssetSerializer(many=True, required=False)

    class Meta:
        model = Distribution
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method in ["PUT", "PATCH"]:
            self.fields["products"].read_only = True

    def validate(self, attrs):
        if not self.instance and not attrs.get("products"):
            raise serializers.ValidationError({"products": "This field is required."})
        return attrs

    def create(self, validated_data):
        products_data = validated_data.pop("products", [])
        assets_data = validated_data.pop("assets", [])

        distribution = Distribution.objects.create(**validated_data)

        for product_data in products_data:
            DistributionProduct.objects.create(
                distribution=distribution, **product_data
            )

        for asset_data in assets_data:
            DistributionAsset.objects.create(distribution=distribution, **asset_data)

        distribution.save()
        return distribution

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["products"] = DistributionProductSerializer(
            instance.products.all(), many=True
        ).data
        representation["assets"] = DistributionAssetSerializer(
            instance.assets.all(), many=True
        ).data
        return representation
