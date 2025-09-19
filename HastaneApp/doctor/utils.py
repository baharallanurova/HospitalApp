from django.db.models import Q
from .models import Patient


def search_patients(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        patients = Patient.objects.filter(
            Q(patient_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    else:
        patients = Patient.objects.all()

    return patients, search_query