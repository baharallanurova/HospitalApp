from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('', views.doctor_login, name='login'),
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.doctor_profile_settings, name='profile'),
    path('change-password/<int:pk>/', views.doctor_change_password, name='change-password'),
    path('profile-settings/', views.doctor_profile_settings, name='profile-settings'),
    path('register/', views.doctor_register, name='register'),
    path('logout/', views.logout_doctor, name='logout'),
    path('patients/', views.my_patients, name='patients'),
    path('schedule-timings/', views.schedule_timings, name='schedule-timings'),
    path('patient-id/', views.my_patients, name='patient-id'),
    path('patient-profile/<int:pk>/', views.my_patients, name='patient-profile'),
    path('education/delete/<int:pk>/', views.delete_education, name='delete-education'),
    path('experience/delete/<int:pk>/', views.delete_experience, name='delete-experience'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointment/accept/<int:pk>/', views.accept_appointment, name='accept-appointment'),
    path('appointment/reject/<int:pk>/', views.reject_appointment, name='reject-appointment'),
    path('patient-search/<int:pk>/', views.my_patients, name='patient-search'),
    path('review/<int:pk>/', views.doctor_dashboard, name='review'),
    path('tests/', views.doctor_test_list, name='test-list'),
    path('prescription/view/<int:pk>/', views.doctor_required, name='view-prescription'),
    path('report/view/<int:pk>/', views.doctor_dashboard, name='view-report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)