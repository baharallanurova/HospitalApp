from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_hospital_admin = models.BooleanField(default=False)
    is_labworker = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)
    login_status = models.BooleanField(default=False)


class Hospital_Information(models.Model):
    HOSPITAL_TYPE = (
        ('private', 'Private hospital'),
        ('public', 'Public hospital'),
    )

    hospital_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(upload_to='hospitals/', default='hospitals/default.png', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    hospital_type = models.CharField(max_length=200, choices=HOSPITAL_TYPE)
    general_bed_no = models.IntegerField(null=True, blank=True)
    available_icu_no = models.IntegerField(null=True, blank=True)
    regular_cabin_no = models.IntegerField(null=True, blank=True)
    emergency_cabin_no = models.IntegerField(null=True, blank=True)
    vip_cabin_no = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='patient')
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(upload_to='patients/', default='patients/user-default.png', null=True,
                                       blank=True)
    blood_group = models.CharField(max_length=200, null=True, blank=True)
    history = models.CharField(max_length=200, null=True, blank=True)
    dob = models.CharField(max_length=200, null=True, blank=True)
    nid = models.CharField(max_length=200, null=True, blank=True)
    serial_number = models.CharField(max_length=200, null=True, blank=True)

    # Chat
    login_status = models.CharField(max_length=200, null=True, blank=True, default="offline")

    def __str__(self):
        return str(self.user.username)
