# accesshub/adapters.py


# ADAPTER PATTERN + DOMAIN LOGIC


# definição da lógica de negócios
# interrompendo o comportamento padrão (fluxos internos) do allauth

# adapters chamados automaticamente pelo allauth em settings.py
# ACCOUNT_ADAPTER = 'accesshub.adapters.MyAccountAdapter'
# SOCIALACCOUNT_ADAPTER = 'accesshub.adapters.MySocialAccountAdapter'  

import os
import secrets
import string

# adapter padrão de login social do Allauth
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# adapter padrão de contas (signup/login manual) do alauth
from allauth.account.adapter import DefaultAccountAdapter
# model padrão de User do Django
from django.contrib.auth.models import User

# adapter customizado p/ login social
# motivo: evitar duplicação de contas
# 
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    # metodo de chamada automatica antes do login via google/github
    def pre_social_login(self, request, sociallogin):
        # Se a conta social já estiver vinculada, não faz nada
        if sociallogin.is_existing:
            return

        email = sociallogin.user.email
        if email:
            # pega o primeiro usuário com este e-mail
            user = User.objects.filter(email=email).first()
            if user:
                # vincula e conecta o login do Google/GitHub ao usuário do banco
                sociallogin.connect(request, user)



# adapter customizado p/ signup/login manual (email + senha)
class MyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Personalização da criação do usuário:
        Define is_active = False (requer confirmação)
        Iguala username ao email para evitar conflitos
        """
        user = super().save_user(request, user, form, commit=False)
        user.is_active = False
        user.username = user.email

        if commit:
            user.save()
        return user

    def generate_email_verification_code(self)
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # log
        print(f"DEBUG_OTP: Código gerado: {code}")
        return code

    def render_mail(self, template_prefix, email, context, headers=None):
        if 'key' in context:
            context['otp_code'] = context['key']
        
        return super().render_mail(template_prefix, email, context, headers)

    def respond_user_inactive(self, request, user):
        return None