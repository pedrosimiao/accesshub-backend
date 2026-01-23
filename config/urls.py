# config/urls.py

from django.contrib import admin
from django.urls import path, include

from accesshub.views import get_csrf_token
from accesshub.auth_views import CustomLoginView, VerifyEmailCodeView
from allauth.account.views import confirm_email
from django.contrib.sites.models import Site # Importe o modelo

# --- BLOCO DE REPARO TEMPORÁRIO ---
try:
    # Tenta garantir que o Site 1 exista para o allauth não quebrar
    Site.objects.get_or_create(
        id=1, 
        defaults={
            'domain': 'accesshub-backend-pqio.onrender.com', 
            'name': 'AccessHub'
        }
    )
except Exception:
    pass 
# ----------------------------------

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

    # ========================
    # Dummies para evitar NoReverseMatch (Allauth interno)
    # ========================
    path("api/v1/auth/inactive/", lambda r: None, name="account_inactive"),
    path("api/v1/auth/confirm-email-sent/", lambda r: None, name="account_email_verification_sent"),
]

