# config/urls.py

# denfinindo endpoints - portas de entrada da API

# painel admin
from django.contrib import admin
# funçoes de definição de rotas
from django.urls import path, include

# views
from accesshub.views import get_csrf_token
from allauth.account.views import confirm_email

# lista de urls do projeti
urlpatterns = [
    # rota p/ painel admin do Django
    path("admin/", admin.site.urls),
    
    # endpoints REST de autenticação (login/logout/user)
    path("api/v1/auth/", include("dj_rest_auth.urls")),

    # endpoint de entrega do token ao browser
    path('api/v1/auth/csrf/', get_csrf_token, name='get_csrf_token'),

    # endpoints de registro (signup)
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),

    # dj-rest-auth busca a lógica de verificação
    path("api/v1/auth/registration/account-confirm-email/<str:key>/", confirm_email, name="account_confirm_email"),

    # endpoints de login social google & github
    path("api/v1/auth/", include("allauth.socialaccount.providers.google.urls")),
    path("api/v1/auth/", include("allauth.socialaccount.providers.github.urls")),
]
