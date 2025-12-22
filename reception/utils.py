from .models import Appointment
from django.utils import timezone

def get_next_token_for_doctor(doctor, appointment_date):
    last = Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date).order_by('-token_number').first()
    return 1 if not last else last.token_number + 1

def expire_old_tokens():
    now = timezone.now()
    actives = Appointment.objects.filter(status='ACTIVE')
    for ap in actives:
        elapsed = (now - ap.created_at).total_seconds() / 60.0
        if elapsed > 15:  # default 15 min
            ap.status = 'COMPLETED'
            ap.save()
