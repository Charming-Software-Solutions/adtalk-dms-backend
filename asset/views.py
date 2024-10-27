from django.shortcuts import render

from asset.models import Asset, AssetType
from asset.serializers import AssetSerializer, AssetTypeSerialiezr
from shared.generic_viewset import GenericViewset


class AssetTypeViewset(GenericViewset):
    include_list_view = True
    protected_views = ["all"]
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerialiezr


class AssetViewset(GenericViewset):
    include_list_view = True
    protected_views = ["all"]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
