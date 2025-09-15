from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from doctor.models import Doctor_Information, Appointment
from hospital.models import Patient
from .models import ChatMessage


@login_required
def chat_home(request, pk=None):
    user = request.user
    context = {
        "page": "home",
        "chat_id": request.GET.get('u', 0),
        "search_query": request.GET.get('search', '')
    }

    if user.is_patient:
        patient = get_object_or_404(Patient, user=user)
        appointments = Appointment.objects.filter(
            patient=patient,
            appointment_status='confirmed'
        ).select_related('doctor')

        doctors = Doctor_Information.objects.filter(
            appointment__in=appointments
        ).distinct()

        context.update({
            "patient": patient,
            "doctors": doctors,
            "appointments": appointments,
        })

        if 'u' in request.GET:
            doctor_id = request.GET['u']
            doctor = get_object_or_404(Doctor_Information, user_id=doctor_id)

            chats = ChatMessage.objects.filter(
                Q(user_from=user, user_to_id=doctor_id) |
                Q(user_from_id=doctor_id, user_to=user)
            ).order_by('date_created')

            context.update({
                "chats": chats,
                "current_chat_user": doctor,
            })

        elif 'search' in request.GET:
            query = request.GET.get('search')
            doctors = Doctor_Information.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )
            context["doctors"] = doctors

        return render(request, "chat/chat_patient.html", context)

    elif user.is_doctor:
        doctor = get_object_or_404(Doctor_Information, user=user)
        appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_status='confirmed'
        ).select_related('patient')

        patients = Patient.objects.filter(
            appointment__in=appointments
        ).distinct()

        context.update({
            "doctor": doctor,
            "patients": patients,
            "appointments": appointments,
        })

        if 'u' in request.GET:
            patient_id = request.GET['u']
            patient = get_object_or_404(Patient, user_id=patient_id)

            chats = ChatMessage.objects.filter(
                Q(user_from=user, user_to_id=patient_id) |
                Q(user_from_id=patient_id, user_to=user)
            ).order_by('date_created')

            context.update({
                "chats": chats,
                "current_chat_user": patient,
            })

        elif 'search' in request.GET:
            query = request.GET.get('search')
            patients = Patient.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            )
            context["patients"] = patients

        return render(request, "doctor-profile.html", context)

    else:
        raise PermissionDenied("Bu sayfaya erişim izniniz yok")


@login_required
def profile(request):
    return render(request, "chat/profile.html", {"page": "profile"})


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def get_messages(request):
    try:
        last_id = int(request.POST.get('last_id', 0))
        chat_id = int(request.POST.get('chat_id', 0))

        if not chat_id:
            return JsonResponse({"error": "Geçersiz sohbet ID'si"}, status=400)

        chats = ChatMessage.objects.filter(
            Q(id__gt=last_id),
            Q(user_from=request.user, user_to_id=chat_id) |
            Q(user_from_id=chat_id, user_to=request.user)
        ).order_by('date_created')

        unread_messages = chats.filter(is_read=False, user_to=request.user)
        unread_messages.update(is_read=True)

        new_msgs = []
        for chat in chats:
            new_msgs.append({
                'id': chat.id,
                'user_from': chat.user_from.id,
                'user_to': chat.user_to.id,
                'message': chat.message,
                'date_created': chat.date_created.strftime("%b-%d-%Y %H:%M"),
                'is_read': chat.is_read,
            })

        return JsonResponse(new_msgs, safe=False)

    except (ValueError, TypeError) as e:
        return JsonResponse({"error": "Geçersiz parametreler"}, status=400)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def send_chat(request):
    try:
        user_from_id = request.POST.get('user_from')
        user_to_id = request.POST.get('user_to')
        message = request.POST.get('message', '').strip()

        if not all([user_from_id, user_to_id, message]):
            return JsonResponse({"status": "failed", "error": "Eksik parametreler"})

        if int(user_from_id) != request.user.id:
            return JsonResponse({"status": "failed", "error": "Yetkisiz işlem"})

        chat_message = ChatMessage.objects.create(
            user_from_id=user_from_id,
            user_to_id=user_to_id,
            message=message
        )

        return JsonResponse({
            "status": "success",
            "message_id": chat_message.id,
            "date_created": chat_message.date_created.strftime("%b-%d-%Y %H:%M")
        })

    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)})


@login_required
def get_conversations(request):
    user = request.user

    conversations = ChatMessage.objects.filter(
        Q(user_from=user) | Q(user_to=user)
    ).order_by('date_created').select_related('user_from', 'user_to')

    conversation_dict = {}
    for msg in conversations:
        other_user = msg.user_from if msg.user_to == user else msg.user_to
        if other_user.id not in conversation_dict:
            conversation_dict[other_user.id] = {
                'user': other_user,
                'last_message': msg,
                'unread_count': 0
            }
        else:
            if msg.date_created > conversation_dict[other_user.id]['last_message'].date_created:
                conversation_dict[other_user.id]['last_message'] = msg

        if msg.user_to == user and not msg.is_read:
            conversation_dict[other_user.id]['unread_count'] += 1

    return JsonResponse(list(conversation_dict.values()), safe=False)