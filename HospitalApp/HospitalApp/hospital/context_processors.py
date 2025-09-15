from django.conf import settings

def global_settings(request):
    return {
        'SITE_NAME': settings.STORE_NAME,
        'DEBUG': settings.DEBUG,
    }