# accesshub/serializers.py


# APPLICATION/CONTRACT LAYER

# customizando o contrato entre frontend/backend

# remoção do campo username

# frontend envia: 
# email 
# password1 (senha)
# password2 (confirmação de senha)

import secrets
import string
from django.conf import settings
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.adapter import get_adapter

class CustomRegisterSerializer(RegisterSerializer):
    username = None 

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.pop('username', None)
        return data

    def validate_username(self, _username):
        return None

    def save(self, request):
        # cria o User e o EmailAddress no banco
        user = super().save(request)
        
        try:
            print(f"🕵️ [SERIALIZER] User {user.email} salvo. Forçando geração de código de 6 dígitos...")

            # busca o objeto EmailAddress vinculado ao user que recém criado
            email_address = EmailAddress.objects.filter(user=user, email=user.email).first()

            if email_address:
                # geração manual do código de 6 dígitos
                # fix: fluxos internos instáveis
                otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
                
                # REGISTRO DE CONFIRMAÇÃO DIRETAMENTE NO BANCO
                # .objects.create() para que o campo 'key' seja o código
                confirmation = EmailConfirmation.objects.create(
                    email_address=email_address,
                    key=otp_code
                )
                
                print(f"🔥 [SERIALIZER_FORCED] CÓDIGO GRAVADO: {otp_code} para {user.email}")
                
                # .send() usa adapter.render_mail para formatar o e-mail
                confirmation.send(request, signup=True)
                
                print(f"✅ [SERIALIZER] Processo de confirmação concluído com sucesso.")
            else:
                print(f"⚠️ [SERIALIZER_ERROR] EmailAddress não encontrado para {user.email}")

        except Exception as e:
            import traceback
            print(f"❌ [SERIALIZER_ERROR] Falha crítica no fluxo de confirmação:")
            print(traceback.format_exc())
            
        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'extra_email_context': {
                'frontend_url': settings.FRONTEND_BASE,
            }
        }
        self.reset_form.save(**opts)