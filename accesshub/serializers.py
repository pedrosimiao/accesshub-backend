# accesshub/serializers.py


# APPLICATION/CONTRACT LAYER

# customizando o contrato entre frontend/backend

# remoção do campo username

# frontend envia: 
# email 
# password1 (senha)
# password2 (confirmação de senha)

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter # Adicionado
from allauth.account import app_settings as allauth_settings

class CustomRegisterSerializer(RegisterSerializer):
    username = None 

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.pop('username', None)
        return data

    def validate_username(self, _username):
        return None

    def save(self, request):
        # salva o user no banco
        user = super().save(request)
        
        # fluxo manual e seguro para disparar o e-mail
        try:
            # valida que o objeto EmailAddress existe no banco
            setup_user_email(request, user, [])
            
            # remove send_email_confirmation (que mudou de lugar),
            # usar o próprio adapter para disparar o e-mail
            # p/ garantir que o generate_email_confirmation_key seja chamado!
            adapter = get_adapter(request)
            adapter.send_confirmation_mail(request, user, signup=True)
            
            print(f"✅ [SERIALIZER] E-mail de confirmação disparado via Adapter para {user.email}")
            
        except Exception as e:
            import traceback
            print(f"❌ [SERIALIZER_ERROR] Erro detalhado:")
            print(traceback.format_exc())
            
        return user