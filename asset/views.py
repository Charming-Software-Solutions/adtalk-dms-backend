from rest_framework import permissions

from asset.models import Asset, AssetType
from asset.serializers import AssetSerializer, AssetTypeSerialiezr
from shared.generic_viewset import GenericViewset
from shared.permissions import IsLogisticsOrAdmin


class AssetTypeViewset(GenericViewset):
    include_list_view = True
    protected_views = ["all"]
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerialiezr

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsLogisticsOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class AssetViewset(GenericViewset):
    include_list_view = True
    protected_views = ["all"]
    queryset = Asset.objects.all().order_by("-updated_at")
    serializer_class = AssetSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsLogisticsOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
