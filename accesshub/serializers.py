# accesshub/serializers.py

# contrato da API
# customizando o contrato entre frontend/backend

# frontend envia: 
# email 
# password1 (senha)
# password2 (confirmação de senha)
# backend não espera mais username

# serializer padrao de registro (dj-rest-auth)
from dj_rest_auth.registration.serializers import RegisterSerializer
# modulo base de serializers do DRF
from rest_framework import serializers

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
