import random
import string
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q, Count
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from hospital.models import User
from .forms import DoctorUserCreationForm
from .models import (
    Doctor_Information, Appointment, Education, Experience,

)


def generate_random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.User.is_doctor:
            messages.error(request, 'Bu sayfaya erişim yetkiniz yok')
            return redirect('doctor-login')
        return view_func(request, *args, **kwargs)

    return wrapper


def send_appointment_email(patient_email, subject, template_name, context):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    try:
        send_mail(
            subject,
            plain_message,
            'hospital_admin@gmail.com',
            [patient_email],
            html_message=html_message,
            fail_silently=False
        )
        return True
    except BadHeaderError:
        return False


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def doctor_change_password(request, pk):
    doctor = get_object_or_404(Doctor_Information, user_id=pk)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "Şifre başarıyla değiştirildi")
            return redirect("doctor-dashboard")
        else:
            messages.error(request, "Yeni şifre ve onay şifresi eşleşmiyor")

    return render(request, 'doctor-change-password.html', {'doctor': doctor})


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def schedule_timings(request):
    doctor = get_object_or_404(Doctor_Information, user=request.user)
    return render(request, 'schedule-timings.html', {'doctor': doctor})


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_doctor(request):
    if request.user.is_authenticated and request.User.is_doctor:
        request.user.login_status = "offline"
        request.user.save()
        logout(request)
        messages.success(request, 'Çıkış yapıldı')
    return redirect('doctor-login')


@csrf_exempt
def doctor_register(request):
    if request.user.is_authenticated:
        return redirect('doctor-dashboard')

    form = DoctorUserCreationForm()

    if request.method == 'POST':
        form = DoctorUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True
            user.save()
            messages.success(request, 'Doktor hesabı oluşturuldu!')
            return redirect('doctor-login')
        else:
            messages.error(request, 'Kayıt sırasında bir hata oluştu')

    return render(request, 'doctor-register.html', {'form': form})


@csrf_exempt
def doctor_login(request):
    if request.user.is_authenticated and request.User.is_doctor:
        return redirect('doctor-dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and User.is_doctor:
            login(request, user)
            messages.success(request, 'Hoş geldiniz Doktor!')
            return redirect('doctor-dashboard')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre')

    return render(request, 'doctor-login.html')


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor_Information, user=request.user)
    current_date = date.today()
    current_date_str = str(current_date)

    today_appointments = Appointment.objects.filter(
        date=current_date_str,
        doctor=doctor,
        appointment_status='confirmed'
    )

    next_date = current_date + timedelta(days=1)
    next_date_str = str(next_date)
    next_days_appointment = Appointment.objects.filter(
        date=next_date_str,
        doctor=doctor
    ).filter(
        Q(appointment_status='pending') | Q(appointment_status='confirmed')
    ).count()

    today_patient_count = Appointment.objects.filter(
        date=current_date_str,
        doctor=doctor
    ).aggregate(count=Count('patient', distinct=True))

    total_appointments_count = Appointment.objects.filter(
        doctor=doctor
    ).aggregate(count=Count('id'))

    context = {
        'doctor': doctor,
        'today_appointments': today_appointments,
        'today_patient_count': today_patient_count,
        'total_appointments_count': total_appointments_count,
        'next_days_appointment': next_days_appointment,
        'current_date': current_date_str,
        'next_date': next_date_str
    }

    return render(request, 'doctor-dashboard.html', context)


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def appointments(request):
    doctor = get_object_or_404(Doctor_Information, user=request.user)
    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_status='pending'
    ).order_by('date')

    return render(request, 'appointments.html', {
        'doctor': doctor,
        'appointments': appointments
    })


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def accept_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.appointment_status = 'confirmed'
    appointment.save()

    email_context = {
        "email": appointment.patient.email,
        "name": appointment.patient.name,
        "username": appointment.patient.username,
        "serial_number": appointment.patient.serial_number,
        "doctor_name": appointment.doctor.name,
        "appointment_serial_num": appointment.serial_number,
        "appointment_date": appointment.date,
        "appointment_time": appointment.time,
        "appointment_status": appointment.appointment_status,
    }

    if send_appointment_email(
            appointment.patient.email,
            "Randevu Onay E-postası",
            'appointment_accept_mail.html',
            email_context
    ):
        messages.success(request, 'Randevu onaylandı ve hasta bilgilendirildi')
    else:
        messages.warning(request, 'Randevu onaylandı ancak e-posta gönderilemedi')

    return redirect('appointments')


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    appointment.appointment_status = 'cancelled'
    appointment.save()

    email_context = {
        "email": appointment.patient.email,
        "name": appointment.patient.name,
        "doctor_name": appointment.doctor.name,
    }

    if send_appointment_email(
            appointment.patient.email,
            "Randevu Reddi E-postası",
            'appointment_reject_mail.html',
            email_context
    ):
        messages.info(request, 'Randevu reddedildi ve hasta bilgilendirildi')
    else:
        messages.warning(request, 'Randevu reddedildi ancak e-posta gönderilemedi')

    return redirect('appointments')


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def delete_education(request, pk):
    education = get_object_or_404(Education, education_id=pk)
    education.delete()
    messages.success(request, 'Eğitim bilgisi silindi')
    return redirect('doctor-profile-settings')


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def delete_experience(request, pk):
    experience = get_object_or_404(Experience, experience_id=pk)
    experience.delete()
    messages.success(request, 'Deneyim bilgisi silindi')
    return redirect('doctor-profile-settings')


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def doctor_profile_settings(request):
    doctor = get_object_or_404(Doctor_Information, user=request.user)

    if request.method == 'GET':
        educations = Education.objects.filter(doctor=doctor)
        experiences = Experience.objects.filter(doctor=doctor)

        return render(request, 'doctor-profile-settings.html', {
            'doctor': doctor,
            'educations': educations,
            'experiences': experiences
        })

    elif request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.phone_number = request.POST.get('number')
        doctor.gender = request.POST.get('gender')
        doctor.dob = request.POST.get('dob')
        doctor.description = request.POST.get('description')
        doctor.consultation_fee = request.POST.get('consultation_fee')
        doctor.report_fee = request.POST.get('report_fee')
        doctor.nid = request.POST.get('nid')
        doctor.visiting_hour = request.POST.get('visit_hour')

        if 'featured_image' in request.FILES:
            doctor.featured_image = request.FILES['featured_image']

        doctor.save()

        degrees = request.POST.getlist('degree')
        institutes = request.POST.getlist('institute')
        year_completes = request.POST.getlist('year_complete')

        for i in range(len(degrees)):
            if degrees[i] and institutes[i] and year_completes[i]:
                Education.objects.create(
                    doctor=doctor,
                    degree=degrees[i],
                    institute=institutes[i],
                    year_of_completion=year_completes[i]
                )

        hospital_names = request.POST.getlist('hospital_name')
        start_years = request.POST.getlist('from')
        end_years = request.POST.getlist('to')
        designations = request.POST.getlist('designation')

        for i in range(len(hospital_names)):
            if hospital_names[i] and start_years[i] and designations[i]:
                Experience.objects.create(
                    doctor=doctor,
                    work_place_name=hospital_names[i],
                    from_year=start_years[i],
                    to_year=end_years[i],
                    designation=designations[i]
                )

        messages.success(request, 'Profil başarıyla güncellendi')
        return redirect('doctor-profile-settings')


@csrf_exempt
@login_required(login_url="doctor-login")
@doctor_required
def my_patients(request):
    doctor = get_object_or_404(Doctor_Information, user=request.user)
    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_status='confirmed'
    )

    return render(request, 'my-patients.html', {
        'doctor': doctor,
        'appointments': appointments
    })


@csrf_exempt
@login_required(login_url="login")
@doctor_required
def doctor_test_list(request):
    doctor = get_object_or_404(Doctor_Information, user=request.user)

    return render(request, 'doctor-test-list.html', {
        'doctor': doctor,
    })


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.login_status = True
    user.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.login_status = False
    user.save()