# accesshub/serializers.py


# APPLICATION/CONTRACT LAYER

# customizando o contrato entre frontend/backend

# remoção do campo username

# frontend envia: 
# email 
# password1 (senha)
# password2 (confirmação de senha)

# serializer padrao de registro (dj-rest-auth)
from dj_rest_auth.registration.serializers import RegisterSerializer

# modulo de confirmação do signup do allauth
from allauth.account.utils import complete_signup

from allauth.account import app_settings as allauth_settings

# serializer customizado 
# herda comportamento padrão do serializer dj-rest-auth
class CustomRegisterSerializer(RegisterSerializer):
    # remove campo username 
    # p/ não ser validado/obrigatório
    username = None

    # metodo p/ remocao do username -> "limpar dados"
    def get_cleaned_data(self):
        # chama o metodo original -> super().get_cleaned_data()
        data = super().get_cleaned_data()
        # remove o campo username
        data.pop('username', None)
        # retorna apenas email e senha
        return data

    # metodo p/  desativar a validação de username do Allauth/DRF
    def validate_username(self, _username):
        return None

    def save(self, request):
        # salva user (chama seu MyAccountAdapter.save_user)
        user = super().save(request)
        
        # finaliza o processo de registro do Allauth.
        # dispara o envio de e-mail, gerando o código de 6 dígitos.
        complete_signup(
            request, 
            user, 
            allauth_settings.EMAIL_VERIFICATION, 
            None
        )
        
        print(f"📢 [SERIALIZER] complete_signup executado com sucesso para {user.email}")
        return user    