# accesshub/adapters.py


# ADAPTER PATTERN + DOMAIN LOGIC


# definição da lógica de negócios
# interrompendo o comportamento padrão (fluxos internos) do allauth

# adapters chamados automaticamente pelo allauth em settings.py
# ACCOUNT_ADAPTER = 'accesshub.adapters.MyAccountAdapter'
# SOCIALACCOUNT_ADAPTER = 'accesshub.adapters.MySocialAccountAdapter'  

import secrets
import string
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User

# Print para confirmar nos logs do Render que o arquivo foi lido
print("🚀 [SISTEMA] Adapters carregados com sucesso!")

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Evita duplicidade: vincula conta social ao e-mail existente."""
        if sociallogin.is_existing:
            return
        email = sociallogin.user.email
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                print(f"🔗 [SOCIAL] Vinculando {email} ao provedor {sociallogin.account.provider}")
                sociallogin.connect(request, user)

class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """Fluxo central de criação de usuário."""
        user = super().save_user(request, user, form, commit=False)
        
        # Se NÃO for login social, desativamos para exigir OTP.
        # Se FOR social, ativamos imediatamente.
        if not hasattr(request, 'sociallogin'):
            print(f"⏳ [MANUAL] Criando usuário inativo: {user.email}")
            user.is_active = False
        else:
            print(f"✅ [SOCIAL] Criando usuário ATIVO: {user.email}")
            user.is_active = True
            
        user.username = user.email
        if commit:
            user.save()
        return user

    def generate_email_confirmation_key(self, email):
        """Gera o código de 6 dígitos em vez da hash de 64 caracteres."""
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        print(f"🔥 [OTP_DEBUG] Código gerado para {email}: {code}")
        return code

    def render_mail(self, template_prefix, email, context, headers=None):
        """Injeta o código (key) na variável otp_code do seu HTML."""
        if 'key' in context:
            context['otp_code'] = context['key']
        print(f"📧 [EMAIL_DEBUG] Enviando e-mail de confirmação para {email}")
        return super().render_mail(template_prefix, email, context, headers)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Retorna apenas o código, limpando a URL de link longo."""
        return emailconfirmation.key