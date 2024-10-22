"""
URL configuration for adtalk_backend_mockup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

api_prefix = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{api_prefix}auth/", include("shared.auth.urls")),
    path(f"{api_prefix}user/", include("users.urls")),
    path(f"{api_prefix}product/", include("product.urls")),
    path(f"{api_prefix}distribution/", include("distribution.urls")),
    path(f"{api_prefix}task/", include("task.urls")),
]
