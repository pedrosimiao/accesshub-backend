# accesshub/views.py

from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    # forçar o Django a enviar o Set-Cookie: csrftoken
    return JsonResponse({"detail": "CSRF cookie set"})