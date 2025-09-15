
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

AUTH_USER_MODEL = 'hospital.User'

class User(AbstractUser):
    is_patient = models.BooleanField(default=False, verbose_name=_('Patient'))
    is_doctor = models.BooleanField(default=False, verbose_name=_('Doctor'))
    is_hospital_admin = models.BooleanField(default=False, verbose_name=_('Hospital Admin'))
    is_labworker = models.BooleanField(default=False, verbose_name=_('Lab Worker'))
    is_pharmacist = models.BooleanField(default=False, verbose_name=_('Pharmacist'))
    login_status = models.BooleanField(default=False, verbose_name=_('Login Status'))

    groups = models.ManyToManyField(
        Group,
        related_name='hospital_users',
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups')
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='hospital_user_permissions',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class Hospital_Information(models.Model):
    class HospitalType(models.TextChoices):
        PRIVATE = 'private', _('Private Hospital')
        PUBLIC = 'public', _('Public Hospital')

    hospital_id = models.AutoField(primary_key=True, verbose_name=_('Hospital ID'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    address = models.CharField(max_length=200, verbose_name=_('Address'))
    featured_image = models.ImageField(
        upload_to='hospitals/',
        default='hospitals/default.png',
        verbose_name=_('Featured Image')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    email = models.EmailField(verbose_name=_('Email'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'))
    hospital_type = models.CharField(
        max_length=10,
        choices=HospitalType.choices,
        verbose_name=_('Hospital Type')
    )
    general_bed_no = models.PositiveIntegerField(default=0, verbose_name=_('General Beds'))
    available_icu_no = models.PositiveIntegerField(default=0, verbose_name=_('Available ICU Beds'))
    regular_cabin_no = models.PositiveIntegerField(default=0, verbose_name=_('Regular Cabins'))
    emergency_cabin_no = models.PositiveIntegerField(default=0, verbose_name=_('Emergency Cabins'))
    vip_cabin_no = models.PositiveIntegerField(default=0, verbose_name=_('VIP Cabins'))

    class Meta:
        verbose_name = _('Hospital Information')
        verbose_name_plural = _('Hospital Information')

    def __str__(self):
        return self.name

class Patient(models.Model):
    class BloodGroup(models.TextChoices):
        A_POSITIVE = 'A+', _('A+')
        A_NEGATIVE = 'A-', _('A-')
        B_POSITIVE = 'B+', _('B+')
        B_NEGATIVE = 'B-', _('B-')
        AB_POSITIVE = 'AB+', _('AB+')
        AB_NEGATIVE = 'AB-', _('AB-')
        O_POSITIVE = 'O+', _('O+')
        O_NEGATIVE = 'O-', _('O-')

    patient_id = models.AutoField(primary_key=True, verbose_name=_('Patient ID'))
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        verbose_name=_('User')
    )
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    username = models.CharField(max_length=200, unique=True, verbose_name=_('Username'))
    age = models.PositiveIntegerField(verbose_name=_('Age'))
    email = models.EmailField(verbose_name=_('Email'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'))
    address = models.CharField(max_length=200, verbose_name=_('Address'))
    featured_image = models.ImageField(
        upload_to='patients/',
        default='patients/user-default.png',
        verbose_name=_('Featured Image')
    )
    blood_group = models.CharField(
        max_length=3,
        choices=BloodGroup.choices,
        verbose_name=_('Blood Group')
    )
    medical_history = models.TextField(blank=True, verbose_name=_('Medical History'))
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'))
    nid = models.CharField(max_length=20, unique=True, verbose_name=_('National ID'))
    serial_number = models.CharField(max_length=10, unique=True, verbose_name=_('Serial Number'))
    login_status = models.CharField(
        max_length=10,
        default="offline",
        verbose_name=_('Login Status')
    )

    class Meta:
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')

    def __str__(self):
        return f"{self.name} ({self.serial_number})"