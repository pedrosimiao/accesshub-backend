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
from allauth.account.models import EmailAddress, EmailConfirmation

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
            print(f"🕵️ [SERIALIZER] User {user.email} salvo. Preparando envio de código...")

            # busca o objeto EmailAddress vinculado ao usuário
            # super().save() já criou objeto, então usar .get()
            email_address = EmailAddress.objects.filter(user=user, email=user.email).first()

            if email_address:
                # .create():
                #   chama adapter.generate_email_confirmation_key() (gera os 6 dígitos)
                #   salva o código no banco vinculado ao email
                confirmation = EmailConfirmation.create(email_address)
                
                # envia o email
                # .send() chama o adapter.render_mail() internamente
                confirmation.send(request, signup=True)
                
                print(f"✅ [SERIALIZER] Código de 6 dígitos gerado e enviado para {user.email}")
            else:
                print(f"⚠️ [SERIALIZER_ERROR] EmailAddress não encontrado para {user.email}")

        except Exception as e:
            import traceback
            print(f"❌ [SERIALIZER_ERROR] Falha no fluxo de confirmação:")
            print(traceback.format_exc())
            
        return user