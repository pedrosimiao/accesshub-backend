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
        
        # check: login social usuário nasce ativo
        if hasattr(request, 'sociallogin'):
            print(f"✅ [AUTH] SOCIAL: {user.email} ATIVO.")
            user.is_active = True
        else:
            print(f"⏳ [AUTH] MANUAL: {user.email} INATIVO.")
            user.is_active = False
            
        user.username = user.email
        if commit: user.save()
        return user

    def generate_email_confirmation_key(self, email):
        # método de fallback. 
        # Allauth tenta gerar a chave por conta própria,
        # forçar geração de 6 dígitos.
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        print(f"🔥 [ADAPTER_FALLBACK] Código gerado via Adapter: {code}")
        return code

    def render_mail(self, template_prefix, email, context, headers=None):
        # injetando o código (key) no contexto do template para ser usado como 'otp_code'.
        if 'key' in context:
            # key: o código de 6 dígitos que gravado já no Serializer
            context['otp_code'] = context['key']
            
        print(f"📧 [EMAIL_DEBUG] Renderizando e-mail para {email} com código: {context.get('key')}")
        return super().render_mail(template_prefix, email, context, headers)

    def get_email_confirmation_url(self, request, emailconfirmation):
        # retornar apenas o código.
        return emailconfirmation.key