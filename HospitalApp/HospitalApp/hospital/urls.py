from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.home, name='hospital_home'),
    path('about-us/', views.about, name='about-us'),
    path('search/', views.search, name='search'),
    path('patient-dashboard/', views.patient_dashboard, name='patient-dashboard'),
    path('profile-settings/', views.profile_settings, name='profile-settings'),
    path('patient-register/', views.patient_register, name='patient-register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)