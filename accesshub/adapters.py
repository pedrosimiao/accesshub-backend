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
        user = super().save_user(request, user, form, commit=False)
        
        user.is_active = False
        
        # sinc username & email p evitar erros de integridade
        user.username = user.email

        # se commit=True -> salva user 
        if commit:
            user.save()
        # retorna o user
        return user

    # sobrescrição a geração da chave para ser um código numérico de 6 dígitos
    def generate_email_confirmation_key(self, email):
        # gerando os 6 dígitos
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        # log do Render para cdebugar enquanto o SMTP não liga
        print(f"DEBUG_OTP: O código gerado para {email} é {code}")
        return code


    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # emailconfirmation.key contém os 6 dígitos gerados acima
        otp_code = emailconfirmation.key 
        
        ctx = {
            "user": emailconfirmation.email_address.user,
            "otp_code": otp_code, 
            # fallback para FRONTEND_URL
            "activate_url": f"{os.getenv('FRONTEND_URL', 'http://127.0.0.1:5173')}/confirm-email",
        }
        
        # Allauth busca:
        # account/email/email_confirmation_signup_subject.txt
        # account/email/email_confirmation_signup_message.html
        self.send_mail("account/email/email_confirmation_signup", 
                    emailconfirmation.email_address.email, ctx)

    def respond_user_inactive(self, request, user):
        return None