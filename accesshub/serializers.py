# accesshub/serializers.py


# APPLICATION/CONTRACT LAYER

# customizando o contrato entre frontend/backend

# remoção do campo username

# frontend envia: 
# email 
# password1 (senha)
# password2 (confirmação de senha)

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

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
            print(f"🕵️ [SERIALIZER] User {user.email} salvo via super(). Buscando EmailAddress...")

            # busca o que email address que já existe
            # Isso evita o AssertionError
            if EmailAddress.objects.filter(user=user).exists():
                
                # forçamos o envio do email de confirmação (com código de 6 dígitos)
                adapter = get_adapter(request)
                adapter.send_confirmation_mail(request, user, signup=True)
                
                print(f"✅ [SERIALIZER] E-mail disparado com sucesso para {user.email}")
            else:
                print(f"⚠️ [SERIALIZER] Estranho: EmailAddress não foi criado automaticamente para {user.email}")

        except Exception as e:
            # crítico: logar o erro mas retornar o user para não travar o cadastro
            import traceback
            print(f"❌ [SERIALIZER_ERROR] Erro ao tentar enviar e-mail:")
            print(traceback.format_exc())
            
        return user