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
# modulo base de serializers do DRF
from rest_framework import serializers
# modulo de envio de email do allauth
from allauth.account.utils import setup_user_email

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

    def save(self, request):
        # salva o user user o comportamento default
        user = super().save(request)
        
        # força configuração do e-mail. 
        # MyAccountAdapter forçado a gerar a chave
        setup_user_email(request, user, signup=True)
        return user