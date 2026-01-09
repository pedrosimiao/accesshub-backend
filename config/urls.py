# config/urls.py

# denfinindo endpoints - portas de entrada da API

# painel admin
from django.contrib import admin
# funçoes de definição de rotas
from django.urls import path, include

# lista de urls do projeti
urlpatterns = [
    # rota p/ painel admin do Django
    path("admin/", admin.site.urls),
    
    # endpoints REST de autenticação (login/logout/user)
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    # endpoints de registro (signup)
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),

    # endpoints de login social google & github
    path("api/v1/auth/", include("allauth.socialaccount.providers.google.urls")),
    path("api/v1/auth/", include("allauth.socialaccount.providers.github.urls")),
]
