from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsLogisticsOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["retrieve", "list"]:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in [
            "LOGISTICS_SPECIALIST",
            "admin",
        ]

    def has_object_permission(self, request, view, obj):
        return view.action in ["retrieve", "list"] or request.user.role in [
            "LOGISTICS_SPECIALIST",
            "admin",
        ]


class IsProjectHandlerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["retrieve", "list"]:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in [
            "PROJECT_HANDLER",
            "admin",
        ]

    def has_object_permission(self, request, view, obj):
        return view.action in ["retrieve", "list"] or request.user.role in [
            "PROJECT_HANDLER",
            "admin",
        ]


class IsLogisticsOrWarehouseWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["retrieve", "list"]:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in [
            "LOGISTICS_SPECIALIST",
            "WAREHOUSE_WOKER",
        ]

    def has_object_permission(self, request, view, obj):
        return view.action in ["retrieve", "list"] or request.user.role in [
            "LOGISTICS_SPECIALIST",
            "WAREHOUSE_WOKER",
        ]
