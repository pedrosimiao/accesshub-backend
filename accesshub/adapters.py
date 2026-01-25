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
        user = super().save_user(request, user, form, commit=False)
        # Se for login social, deixa Ativo. Se for manual, desativa.
        user.is_active = hasattr(request, 'sociallogin')
        user.username = user.email
        if commit:
            user.save()
        return user

    def generate_email_confirmation_key(self, email):
        # Isso garante que a 'key' no banco e no e-mail seja 6 dígitos
        return ''.join(secrets.choice(string.digits) for _ in range(6))

    def render_mail(self, template_prefix, email, context, headers=None):
        # Garante que {{ otp_code }} funcione no seu HTML
        if 'key' in context:
            context['otp_code'] = context['key']
        return super().render_mail(template_prefix, email, context, headers)

    def get_email_confirmation_url(self, request, emailconfirmation):
        # Evita que o Allauth tente montar uma URL gigante no e-mail
        return emailconfirmation.key