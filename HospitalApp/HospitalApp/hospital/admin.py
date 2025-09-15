from django.contrib import admin
from .models import User, Hospital_Information, Patient

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_patient', 'is_doctor', 'is_hospital_admin', 'is_labworker', 'is_pharmacist')
    list_filter = ('is_patient', 'is_doctor', 'is_hospital_admin', 'is_labworker', 'is_pharmacist')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Hospital_Information)
class HospitalInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital_type', 'phone_number', 'email')
    list_filter = ('hospital_type',)
    search_fields = ('name', 'address', 'email')
    readonly_fields = ('hospital_id',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'blood_group', 'age')
    search_fields = ('name', 'email', 'phone_number', 'nid')
    readonly_fields = ('patient_id', 'serial_number')