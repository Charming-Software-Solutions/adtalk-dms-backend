from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewset

app_name = "task"

router = DefaultRouter()
router.register(r"", TaskViewset, basename="task")

urlpatterns = [
    path("", include(router.urls)),
]
