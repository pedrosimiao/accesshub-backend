# classe Path: representa caminhos de arquivos
# manipular arquivos e dirs independente do sistema operacional
from pathlib import Path

# # módulo os: acesso a variáveis de ambiente
import os
# load_dotenv: função que carrega variáveis do arquivo .env
from dotenv import load_dotenv

# dj_database_url: configura o db via parsing da 
# string/variável DATABASE_URL (no Render/Koyeb)
import dj_database_url

# lê o arquivo .env e atribui as variáveis de ambiente
load_dotenv()

# pasta raiz = caminho do diretório pai do diretório pai do arquivo atual
# Path(__file__): cria um objeto de caminho que representa o arquivo atual(__file__)
# .resolve(): Resolve o caminho para um caminho absoluto (não contém links simbólicos ou referências relativas como .. ou .)
# .parent: retorna o diretório pai que contém o caminho atual 
# .parent.parent: sobe dois níveis de diretório.
BASE_DIR = Path(__file__).resolve().parent.parent

# chave secreta (p/ cookies, sessions, tokens & hashs)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-development-only-key")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", 
    "localhost,127.0.0.1,"
    ".koyeb.app").split(",")

# apps básicos Django
INSTALLED_APPS = [
    # interface admin
    "django.contrib.admin",
    # sistema de users e auth
    "django.contrib.auth",
    # conteúdos genéricos (permissões,etc.)
    "django.contrib.contenttypes",
    # sessions baseadas em cookies
    "django.contrib.sessions",
    # sistema de msgs
    "django.contrib.messages",
    # arquivos estáticos
    "django.contrib.staticfiles",
    # sistema de sites (usado pelo Allauth para gerar urls)
    "django.contrib.sites", 

    # meu app de autenticação 
    "accesshub.apps.AccesshubConfig",
    # DRF 
    "rest_framework",
    # tokens de autenticação (dj-rest-auth exige)
    "rest_framework.authtoken",
    # comunicação frontend/backend (headers)
    "corsheaders", 
    
    "dj_rest_auth", 
    "allauth",

    # login via email/senha 
    "allauth.account",
    # login social
    "allauth.socialaccount",
    # provedor google
    "allauth.socialaccount.providers.google",
    # provedor github
    "allauth.socialaccount.providers.github",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    
    # middleware do whitenoise p/ lidar com arquivos estaticos
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # middleware p/ lidar com as chamadas do Vite (frontend acessando backend)
    "corsheaders.middleware.CorsMiddleware",
    
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    
    # proteção contra CSRF -> 403 (block requests) se o token não for enviado
    "django.middleware.csrf.CsrfViewMiddleware",
    
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = False

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# if variável DATABASE_URL (Render/Koyeb): 
# sobrescrever com a config do Postgres
database_url = os.getenv("DATABASE_URL")
if database_url:
    DATABASES["default"] = dj_database_url.parse(database_url)


AUTHENTICATION_BACKENDS = [
    # backend padrão django
    'django.contrib.auth.backends.ModelBackend',
    # backend allauth (email, social)
    'allauth.account.auth_backends.AuthenticationBackend',
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# ***** CONFIGURAÇÕES DE COOKIE E CORS (PARA VITE 5173) *****
# ==============================================================================

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS", 
    "http://127.0.0.1:5173"
).split(",")

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", 
    "http://127.0.0.1:5173"
).split(",")

# navegador envia o cookie 'sessionid' para o Django
CORS_ALLOW_CREDENTIALS = True

# 'Lax' permite que o cookie de sessão persista 
# ao redirecionamento (Google OAuth)
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# não havendo domínio definido no .env, usar o ip local
SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN", "127.0.0.1")
CSRF_COOKIE_DOMAIN = os.getenv("CSRF_COOKIE_DOMAIN", "127.0.0.1")

# cookie config (Ajuste fino para HTTPS)
# (quando DEBUG=False) -> cookies seguros.
SESSION_COOKIE_SECURE = not DEBUG 
CSRF_COOKIE_SECURE = not DEBUG

# segurança contra XSS (JavaScript não lê o cookie de sessão)
SESSION_COOKIE_HTTPONLY = True

# false p/ que o Axios (via js-cookie) leia o 'csrftoken'
CSRF_COOKIE_HTTPONLY = False  

# django sempre envia o Cookie CSRF em cada resposta
CSRF_USE_SESSIONS = False

# ==============================================================================
# ALLAUTH & REDIRECTS
# ==============================================================================

SITE_ID = 1 

ACCOUNT_SIGNUP_FIELDS = ['email*']
ACCOUNT_LOGIN_METHODS = {'email'}

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# verificação obrigatória de email
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False


# adapter customizado
ACCOUNT_ADAPTER = 'accesshub.adapters.MyAccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online', 'prompt': 'select_account'},
        'OAUTH_PKCE_ENABLED': True,
        'FETCH_USERINFO': True,
    },
    'github': {
        'SCOPE': ['user:email', 'read:user'],
    },
}

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# URLs de retorno para o frontend
SOCIALACCOUNT_LOGIN_REDIRECT_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173") + "/dashboard"
LOGIN_REDIRECT_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173") + "/dashboard"
LOGOUT_REDIRECT_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173") + "/login"

# adapter customizado
SOCIALACCOUNT_ADAPTER = 'accesshub.adapters.MySocialAccountAdapter'

# ==============================================================================
# REST FRAMEWORK
# ==============================================================================

REST_FRAMEWORK = {
    # autenticação via session
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication', 
    ),
    # user deve estar logado por padrão
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

REST_AUTH = {
    'USE_JWT': False,
    'SESSION_LOGIN': True,
    'REGISTER_SERIALIZER': 'accesshub.serializers.CustomRegisterSerializer',
}

# ==============================================================================
# CONFIGURAÇÃO DE ENVIO DE E-MAIL (NOVO)
# ==============================================================================


# Backend de Console: em dev (if DEBUG) email aparece no terminal 
# onde o servidor roda
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# SMTP externo
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")