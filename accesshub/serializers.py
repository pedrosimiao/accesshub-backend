# accesshub/serializers.py


# APPLICATION/CONTRACT LAYER

# customizando o contrato entre frontend/backend

# remoção do campo username

# frontend envia: 
# email 
# password1 (senha)
# password2 (confirmação de senha)

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.utils import setup_user_email, send_email_confirmation

class CustomRegisterSerializer(RegisterSerializer):
    username = None 

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.pop('username', None)
        return data

    def validate_username(self, _username):
        return None

    def save(self, request):
        # (chama o save_user do Adapter)
        user = super().save(request)
        
        # força a criação do registro de e-mail e o envio
        # ignora qualquer automação que esteja falhando e vai direto
        try:
            # validar EmailAddress existe
            email_address = setup_user_email(request, user, [])
            
            # trigger do envio - generate_email_confirmation_key DEVE 
            # ser chamado
            send_email_confirmation(request, user, signup=True)
            print(f"✅ [DEBUG] Fluxo de e-mail forçado para {user.email}")
            
        except Exception as e:
            print(f"❌ [ERRO] Falha ao disparar e-mail: {str(e)}")
            
        return user