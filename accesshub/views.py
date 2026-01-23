# accesshub/views.py

# INFRA HTTP

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

@ensure_csrf_cookie
def get_csrf_token(request):
    # forçar o Django a enviar o Set-Cookie: csrftoken no Header da resposta
    response = JsonResponse({"detail": "CSRF cookie set"})
    # enviar o token no corpo para debug
    return response