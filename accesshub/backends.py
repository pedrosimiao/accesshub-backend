#  accesshub/backends.py

# AUTHENTICATION BACKEND

from django.contrib.auth.backends import ModelBackend

class VerifiedEmailBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # só autentica se estiver ativo
        return super().user_can_authenticate(user) and user.is_active
