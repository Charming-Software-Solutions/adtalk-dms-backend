from django.urls import include, path
from rest_framework.routers import DefaultRouter

from employee.views import EmployeeViwset

app_name = "employee"

router = DefaultRouter()
router.register(r"", EmployeeViwset, basename="employee")

urlpatterns = [path("", include(router.urls))]
