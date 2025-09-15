from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from doctor.models import Doctor_Information
from .models import Hospital_Information


def search_doctors(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        doctors = Doctor_Information.objects.filter(
            register_status='Accepted'
        ).filter(
            Q(name__icontains=search_query) |
            Q(hospital_name__name__icontains=search_query) |
            Q(department__icontains=search_query)
        ).distinct()
    else:
        doctors = Doctor_Information.objects.filter(register_status='Accepted')
    return doctors, search_query


def search_hospitals(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        hospitals = Hospital_Information.objects.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query)
        ).distinct()
    else:
        hospitals = Hospital_Information.objects.all()
    return hospitals, search_query


def paginate_hospitals(request, hospitals, results_per_page=10):
    page = request.GET.get('page', 1)
    paginator = Paginator(hospitals, results_per_page)

    try:
        paginated_hospitals = paginator.page(page)
    except PageNotAnInteger:
        paginated_hospitals = paginator.page(1)
    except EmptyPage:
        paginated_hospitals = paginator.page(paginator.num_pages)

    left_index = max(1, int(page) - 2)
    right_index = min(paginator.num_pages + 1, int(page) + 3)

    custom_range = range(left_index, right_index)
    return custom_range, paginated_hospitals

