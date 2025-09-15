
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ChatApp/', include('ChatApp.urls')),
    path('doctor/', include('doctor.urls')),
    path('hospital/', include('hospital.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('', include('hospital.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
