# config/urls.py

from django.contrib import admin
from django.urls import path, include

from accesshub.views import get_csrf_token
from accesshub.auth_views import CustomLoginView, VerifyEmailCodeView
from allauth.account.views import confirm_email

urlpatterns = [

    # ========================
    # Admin
    # ========================
    path("admin/", admin.site.urls),

    # ========================
    # Infra
    # ========================
    path("api/v1/auth/csrf/", get_csrf_token, name="get_csrf_token"),

    # ========================
    # Auth base (dj-rest-auth)
    # ========================
    path("api/v1/auth/login/", CustomLoginView.as_view(), name="rest_login"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),

    # ========================
    # Register
    # ========================
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),

    # fallback / compatibilidade allauth
    path(
        "api/v1/auth/registration/account-confirm-email/<str:key>/",
        confirm_email,
        name="account_confirm_email",
    ),

    # ========================
    # Verificação manual por código
    # ========================
    path(
        "api/v1/auth/verify-email/",
        VerifyEmailCodeView.as_view(),
        name="verify_email_code",
    ),

    # ========================
    # Social login
    # ========================
    path("api/v1/auth/", include("allauth.socialaccount.providers.google.urls")),
    path("api/v1/auth/", include("allauth.socialaccount.providers.github.urls")),
]

