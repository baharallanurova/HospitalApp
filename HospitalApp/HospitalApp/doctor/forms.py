from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailField

from hospital.models import User
from .models import Doctor_Information


class DoctorUserCreationForm(UserCreationForm):
    email = EmailField(
        max_length=200,
        help_text='Geçerli bir e-posta adresi giriniz.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': '150 karakter veya daha az. Yalnızca harf, rakam ve @/./+/-/_ karakterleri.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control floating',
            'placeholder': 'Kullanıcı Adı'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control floating',
            'placeholder': 'E-posta Adresi'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control floating',
            'placeholder': 'Şifre'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control floating',
            'placeholder': 'Şifre Tekrar'
        })

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor_Information
        fields = [
            'name', 'email', 'phone_number', 'degree', 'department_name',
            'featured_image', 'visiting_hour', 'consultation_fee',
            'report_fee', 'dob', 'hospital_name', 'gender', 'description'
        ]
        labels = {
            'name': 'Ad Soyad',
            'email': 'E-posta',
            'phone_number': 'Telefon Numarası',
            'department_name': 'Bölüm',
            'visiting_hour': 'Çalışma Saatleri',
            'consultation_fee': 'Muayene Ücreti',
            'report_fee': 'Rapor Ücreti',
            'dob': 'Doğum Tarihi',
            'hospital_name': 'Hastane',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            if field_name == 'phone_number':
                field.widget.attrs['placeholder'] = '05XX XXX XX XX'
            elif field_name == 'visiting_hour':
                field.widget.attrs['placeholder'] = '09:00 - 17:00'