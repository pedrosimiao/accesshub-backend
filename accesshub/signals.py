# accesshub/signals.py

# DOMAIN EVENTS:
# @receiver(post_save, sender=User): user nasce inativo
# @receiver(email_confirmed): ativa o user 


from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from allauth.account.signals import email_confirmed

@receiver(email_confirmed)
def activate_user_on_email_confirmed(request, email_address, **kwargs):
    user = email_address.user
    if not user.is_active:
        user.is_active = True
        user.save()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        # user começa inativo (email confirmation)
        instance.is_active = False
        instance.save()
