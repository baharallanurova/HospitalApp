from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor_Information

@receiver(post_save, sender=Doctor_Information)
def update_doctor_user(sender, instance, created, **kwargs):

    if not created:
        user = instance.user
        if user:
            user.first_name = instance.name
            user.username = instance.username
            user.email = instance.email
            user.save(update_fields=['first_name', 'username', 'email'])