from django.db import models

from hospital.models import Hospital_Information, User, Patient


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doctor_Information(BaseModel):
    DOCTOR_TYPE = (
        ('Cardiologists', 'Kardiyolog'),
        ('Neurologists', 'Nörolog'),
        ('Pediatricians', 'Pediatrist'),
        ('Physiatrists', 'Fizyatrist'),
        ('Dermatologists', 'Dermatolog'),
    )

    doctor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Erkek'), ('female', 'Kadın')))
    description = models.TextField(max_length=1000, blank=True, null=True)
    department_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)

    featured_image = models.ImageField(upload_to='doctors/', default='doctors/user-default.png')
    certificate_image = models.ImageField(upload_to='doctors_certificate/', default='doctors_certificate/default.png')

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    nid = models.CharField(max_length=11, unique=True)
    visiting_hour = models.CharField(max_length=200)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    report_fee = models.DecimalField(max_digits=10, decimal_places=2)
    dob = models.DateField()
    hospital_name = models.ForeignKey(Hospital_Information, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.department_name}"


class Appointment(BaseModel):
    APPOINTMENT_TYPE = (
        ('report', 'Rapor'),
        ('checkup', 'Kontrol'),
    )
    APPOINTMENT_STATUS = (
        ('pending', 'Beklemede'),
        ('confirmed', 'Onaylandı'),
        ('cancelled', 'İptal Edildi'),
    )

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(Doctor_Information, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=10, choices=APPOINTMENT_TYPE)
    appointment_status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS, default='pending')
    serial_number = models.CharField(max_length=10, unique=True)
    payment_status = models.CharField(max_length=10, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date}"


class Education(BaseModel):
    education_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor_Information, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=200)
    institute = models.CharField(max_length=200)
    year_of_completion = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.doctor.name} - {self.degree}"


class Experience(BaseModel):
    experience_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor_Information, on_delete=models.CASCADE, related_name='experiences')
    work_place_name = models.CharField(max_length=200)
    from_year = models.PositiveIntegerField()
    to_year = models.PositiveIntegerField(blank=True, null=True)
    designation = models.CharField(max_length=200)
    currently_working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.name} - {self.work_place_name}"

class Prescription(BaseModel):
    prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey('Doctor_Information', on_delete=models.CASCADE, related_name='given_prescriptions')
    medicines = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription {self.prescription_id} - {self.patient.name}"

