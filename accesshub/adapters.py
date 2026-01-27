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

# Print de inicialização para confirmar que o Render carregou o arquivo
print("🚀 [SISTEMA] accesshub/adapters.py foi carregado!")

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Vincula contas sociais a usuários existentes pelo e-mail
        para evitar erro de 'email já cadastrado'.
        """
        if sociallogin.is_existing:
            return
        
        email = sociallogin.user.email
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                print(f"🔗 [SOCIAL] Vinculando conta {sociallogin.account.provider} ao user: {email}")
                sociallogin.connect(request, user)

class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        O FUNIL: Todo usuário (Social ou Manual) passa por aqui.
        """
        user = super().save_user(request, user, form, commit=False)
        
        # CHECAGEM CRÍTICA:
        # Se vier do Google/GitHub, o objeto 'request' terá o atributo 'sociallogin'
        is_social = hasattr(request, 'sociallogin')
        
        if is_social:
            print(f"✅ [AUTH] Login SOCIAL detectado para {user.email}. Definindo is_active=True")
            user.is_active = True
        else:
            print(f"⏳ [AUTH] Login MANUAL detectado para {user.email}. Definindo is_active=False (aguardando OTP)")
            user.is_active = False
            
        user.username = user.email # Mantém consistência username = email
        
        if commit:
            user.save()
        return user

    def generate_email_confirmation_key(self, email):
        """
        MATA A HASH DE 64 CARACTERES.
        Substitui o token longo por 6 dígitos numéricos.
        """
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        print(f"🔥 [OTP] Código gerado para {email}: {code}")
        return code

    def render_mail(self, template_prefix, email, context, headers=None):
        """Prepara os dados para o template HTML do e-mail"""
        if 'key' in context:
            context['otp_code'] = context['key']
            print(f"📧 [EMAIL] Preparando envio de código {context['key']} para {email}")
        return super().render_mail(template_prefix, email, context, headers)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Retorna apenas o código para evitar que o Allauth monte uma URL de link"""
        return emailconfirmation.key