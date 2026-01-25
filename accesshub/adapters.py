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

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return
        email = sociallogin.user.email
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                sociallogin.connect(request, user)

class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Diferencia o fluxo Social do Manual para evitar o loop de redirecionamento.
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Se for login social (Google/GitHub), deixamos Ativo.
        # Se for manual, desativamos para exigir a ativação por código.
        if hasattr(request, 'sociallogin'):
            user.is_active = True
        else:
            user.is_active = False
            
        user.username = user.email
        if commit:
            user.save()
        return user

    def generate_email_confirmation_key(self, email):
        """
        ESTE MÉTODO MATA A HASH DE 64 CARACTERES.
        O Allauth usa isso para gerar a 'key'. Ao retornar 6 dígitos,
        forçamos o sistema a usar o código numérico no banco e no template.
        """
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        # Com DEBUG=True no Render, este print APARECERÁ nos logs:
        print(f"\n[DEBUG_RENDER] GERANDO CÓDIGO OTP: {code} para o email {email}\n")
        return code

    def render_mail(self, template_prefix, email, context, headers=None):
        """Entrega o código para o template HTML"""
        if 'key' in context:
            context['otp_code'] = context['key']
        return super().render_mail(template_prefix, email, context, headers)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Evita que o Allauth tente criar um link longo no email"""
        return emailconfirmation.key