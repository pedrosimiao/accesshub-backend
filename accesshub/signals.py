# accesshub/signals.py

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        # user começa inativo (email confirmation)
        instance.is_active = False
        instance.save()

        # (futuro): criar perfil
        # Profile.objects.create(user=instance)
        # log, métricas, onboarding, etc
