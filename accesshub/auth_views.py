# acceshub/auth_views.py

from dj_rest_auth.views import LoginView
from accesshub.exceptions import InactiveUserException
from allauth.account.models import EmailConfirmation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# IDENTITY MODULE

# camada de identidade da API


class CustomLoginView(LoginView):
    def login(self):
        # dj-rest-auth preenche self.user apos validacao o serializer
        user = getattr(self, "user", None)

        # se VerifiedEmailBackend não autenticar 
        # (senha errada ou user is None)
        if user is None:
            # super().login() lança o erro 400 padrão
            return super().login()

        # se o user existe mas backends.py ou adapter marcou is_active=False
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
            confirmation = EmailConfirmation.objects.get(key=code)
            confirmation.confirm(request)
            
            user = confirmation.email_address.user
            user.is_active = True
            user.save()
            
            print(f"✅ [AUTH] Usuário {user.email} ativado com sucesso!")
            return Response({"detail": "Account activated"}, status=200)
            
        except EmailConfirmation.DoesNotExist:
            return Response({"detail": "Invalid or expired code"}, status=400)