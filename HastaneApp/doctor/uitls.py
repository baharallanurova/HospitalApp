from django.db.models import Q

from .models import Patient


def searchPatients(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    patient = Patient.objects.filter(
        Q(patient_id__icontains=search_query))

    return patient, search_query
