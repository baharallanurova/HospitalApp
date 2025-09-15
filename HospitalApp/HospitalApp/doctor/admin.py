from django.contrib import admin
from .models import (
    Doctor_Information, Appointment,
    Education, Experience
)

@admin.register(Doctor_Information)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'name', 'email', 'department_name', 'hospital_name')
    list_filter = ('department_name', 'hospital_name')
    search_fields = ('name', 'email', 'phone_number')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'doctor', 'patient', 'appointment_status')
    list_filter = ('appointment_status', 'date')
    search_fields = ('doctor__name', 'patient__name')



admin.site.register(Education)
admin.site.register(Experience)
