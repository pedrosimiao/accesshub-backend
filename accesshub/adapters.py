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

print("🚀 [SISTEMA] Adapters carregados com sucesso!")

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing: return
        email = sociallogin.user.email
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                print(f"🔗 [SOCIAL] Vinculando {email}")
                sociallogin.connect(request, user)

class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        
        # O Ponto Crucial: Diferenciando Manual de Social
        if hasattr(request, 'sociallogin'):
            print(f"✅ [AUTH] SOCIAL: {user.email} ATIVO.")
            user.is_active = True
        else:
            print(f"⏳ [AUTH] MANUAL: {user.email} INATIVO (Aguardando OTP).")
            user.is_active = False
            
        user.username = user.email
        if commit: user.save()
        return user

    def generate_email_confirmation_key(self, email):
        # Gerando os 6 dígitos que a sua VerifyEmailCodeView espera
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        print(f"🔥 [OTP_DEBUG] Código: {code} para {email}")
        return code

    def render_mail(self, template_prefix, email, context, headers=None):
        if 'key' in context:
            context['otp_code'] = context['key']
        return super().render_mail(template_prefix, email, context, headers)

    def get_email_confirmation_url(self, request, emailconfirmation):
        # Retorna apenas os 6 dígitos para o Allauth não tentar montar um link
        return emailconfirmation.key