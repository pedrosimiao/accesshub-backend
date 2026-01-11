# accesshub/adapters.py

# definição da lógica de negócio
# interrompendo o comportamento padrão do allauth

# adapters chamados automaticamente pelo allauth em settings.py
# ACCOUNT_ADAPTER = 'accesshub.adapters.MyAccountAdapter'
# SOCIALACCOUNT_ADAPTER = 'accesshub.adapters.MySocialAccountAdapter'  

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
        # dj-rest-auth signup manual.
        # chama o método original do allauth -> super.save_user(...)
        # impede saving no banco antes do sinc de username e email
        # pois username esta desativado no formulario
        user = super().save_user(request, user, form, commit=False)
        
        # sinc username & email p evitar erros de integridade
        user.username = user.email

        # se commit=True -> salva user 
        if commit:
            user.save()
        # retorna o user
        return user

    # metodo p/ definir url enviada no email
    def get_email_confirmation_url(self, request, emailconfirmation):
        # sobrescricao da url do email para apontar para o frontend React
        # retorna http://127.0.0.1:5173/confirm-email/chave_gerada
        return f"http://127.0.0.1:5173/confirm-email/{emailconfirmation.key}"

    