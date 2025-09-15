import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from doctor.models import Doctor_Information
from pharmacy.models import Pharmacist
from .models import Patient, User

def generate_patient_serial():
    return "#PT" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                if instance.is_patient:
                    Patient.objects.create(
                        user=instance,
                        username=instance.username,
                        email=instance.email,
                        serial_number=generate_patient_serial()
                    )
                elif instance.is_doctor:
                    Doctor_Information.objects.create(
                        user=instance,
                        username=instance.username,
                        email=instance.email
                    )
                elif instance.is_pharmacist:
                    Pharmacist.objects.create(
                        user=instance,
                        username=instance.username,
                        email=instance.email
                    )
        except Exception as e:
            instance.delete()
            raise e

@receiver(post_save, sender=Patient)
def update_patient_user(instance, created):
    if not created:
        user = instance.user
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()