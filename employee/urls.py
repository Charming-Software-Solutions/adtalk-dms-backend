from django.urls import include, path
from rest_framework.routers import DefaultRouter

from employee.views import (
    EmployeeViwset,
    RetrieveOwnEmployeeView,
    UpdateEmployeeProfileView,
)

app_name = "employee"

router = DefaultRouter()
router.register(r"", EmployeeViwset, basename="employee")

urlpatterns = [
    path(
        "update-employee-profile/",
        UpdateEmployeeProfileView.as_view(),
        name="update-employee-profile",
    ),
    path("profile/", RetrieveOwnEmployeeView.as_view(), name="employee-profile"),
    path("", include(router.urls)),
]
