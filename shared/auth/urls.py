from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from .views import ChangeEmailView, ChangePasswordView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="global-login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="global-refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token-blacklist"),
    path("change-email/", ChangeEmailView.as_view(), name="change-email"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
