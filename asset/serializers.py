from rest_framework import serializers

from asset.models import Asset, AssetType


class AssetTypeSerialiezr(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"
