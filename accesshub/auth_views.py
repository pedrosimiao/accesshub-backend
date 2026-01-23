# acceshub/auth_views.py

from dj_rest_auth.views import LoginView
from accesshub.exceptions import InactiveUserException
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# IDENTITY MODULE

# camada de identidade da API


class CustomLoginView(LoginView):
    def login(self):
        user = self.user

        if not user.is_active:
            raise InactiveUserException()

        return super().login()

# orquestração de confirmação de account
class VerifyEmailCodeView(APIView):
    permission_classes = []

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response({"detail": "Code is required"}, status=400)

        try:
            # tenta buscar o código de 6 dígitos na tabela de confirmações
            confirmation = EmailConfirmation.objects.get(key=code)
            confirmation.confirm(request)
        except EmailConfirmation.DoesNotExist:
            # fallback para chaves HMAC (padrão do Allauth se o de cima falhar)
            try:
                confirmation = EmailConfirmationHMAC.from_key(code)
                confirmation.confirm(request)
            except Exception:
                return Response({"detail": "Invalid code"}, status=400)

        # se chegou aqui o e-mail foi confirmado.
        # ativa o usuário que estava is_active=False
        user = confirmation.email_address.user
        user.is_active = True
        user.save()

        return Response({"detail": "Account activated"})