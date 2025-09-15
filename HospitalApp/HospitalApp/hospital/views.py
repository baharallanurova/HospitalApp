from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, PatientForm
from .models import Patient


from django.shortcuts import render

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about-us.html')

def search(request):
    return render(request, 'search.html')

def patient_register(request):
    if request.user.is_authenticated:
        return redirect('hospital:patient-dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.save()

            messages.success(request, _('Hasta hesabı başarıyla oluşturuldu!'))
            return redirect('hospital:login')
        else:
            messages.error(request, _('Kayıt sırasında bir hata oluştu'))
    else:
        form = CustomUserCreationForm()

    return render(request, 'patient-register.html', {'form': form})


@login_required
def patient_dashboard(request):
    if not request.User.is_patient:
        messages.error(request, _('Bu sayfaya erişim izniniz yok'))
        return redirect('hospital:home')

    patient = get_object_or_404(Patient, user=request.user)

    context = {
        'patient': patient,
    }
    return render(request, 'patient-dashboard.html', context)


@login_required
def profile_settings(request):
    if not request.User.is_patient:
        messages.error(request, _('Bu sayfaya erişim izniniz yok'))
        return redirect('hospital:home')

    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profil ayarları başarıyla güncellendi!'))
            return redirect('hospital:patient-dashboard')
        else:
            messages.error(request, _('Lütfen formdaki hataları düzeltin'))
    else:
        form = PatientForm(instance=patient)

    return render(request, 'profile-settings.html', {'form': form, 'patient': patient})


