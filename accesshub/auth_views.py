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


# reenvio do código de validação de conta
class ResendOTPView(APIView):
    """
    Usuário inativo pede um novo código de verificação
    sem precisar refazer o cadastro.
    """
    permission_classes = [] 

    def post(self, request):
        email = request.data.get("email")
        
        # localizando user cadastrado inativo
        user = User.objects.filter(email=email, is_active=False).first()

        if user:
            email_address = EmailAddress.objects.filter(user=user, email=email).first()
            if email_address:
                # novo código de 6 dígitos
                otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
                
                # limpeza de dados antigos não confirmados para este e-mail
                EmailConfirmation.objects.filter(email_address=email_address).delete()
                
                # nova confirmação
                confirmation = EmailConfirmation.objects.create(
                    email_address=email_address,
                    key=otp_code
                )
                
                # envio de e-mail usando o adapter do Allauth
                confirmation.send(request, signup=False)
                return Response({"detail": "Novo código enviado!"}, status=200)
        
        # resposta por segurança (evitando enumeração de usuários)
        return Response({"detail": "Se o e-mail for válido e estiver inativo, um novo código foi enviado."}, status=200)