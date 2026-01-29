# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    InstitutionByCodeView,
    ProfileUpdateView,
    RegisterView,
    MeView,
    UserWalletInfoView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("me/", MeView.as_view(), name="auth-me"),
    path("profile/", ProfileUpdateView.as_view(), name="auth-profile"),
    path("wallet/", UserWalletInfoView.as_view(), name="user-wallet"),
    path(
        "institutions/<str:code>/",
        InstitutionByCodeView.as_view(),
        name="institution-by-code",
    ),
]
