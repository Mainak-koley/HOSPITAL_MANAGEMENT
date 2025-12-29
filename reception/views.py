from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from .models import Appointment, PatientProfile, Prescription, Billing
from .serializers import PatientProfileSerializer, PatientRegisterSerializer, AppointmentSerializer, PrescriptionSerializer, BillingSerializer

User = get_user_model()

def is_patient(user):
    return user.role == 'PATIENT'

def is_doctor(user):
    return user.is_superuser

def is_pharmacist(user):
    return user.is_staff



class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = PatientRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "Patient registered", "id": user.id})

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AppointmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        if request.user.is_superuser:
            qs = Appointment.objects.filter(doctor=request.user,appointment_date=timezone.now().date())
        else:
            qs = Appointment.objects.filter(patient=request.user)

        return Response(AppointmentSerializer(qs, many=True).data)

    def create(self, request):
        if not is_patient(request.user):
            return Response({"error": "Only patients can book"}, status=403)

        doctor_name = request.data.get("doctor_name")
        appointment_date = request.data.get("appointment_date")

        if not doctor_name or not appointment_date:
            return Response({"error": "doctor_name and appointment_date required"},status=400)

        doctor = get_object_or_404(User,username__iexact=doctor_name,is_superuser=True)
        token = Appointment.objects.filter(doctor=doctor,appointment_date=appointment_date).count() + 1
        appointment = Appointment.objects.create(patient=request.user,doctor=doctor,appointment_date=appointment_date,token_number=token)
        return Response(AppointmentSerializer(appointment).data,status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({"error": "Only doctor"}, status=403)

        appointment = get_object_or_404(Appointment, id=pk)
        appointment.status = "COMPLETED"
        appointment.save()

        return Response({"message": "Appointment closed"})




class PrescriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        if user.is_staff: 
            qs = Prescription.objects.all()
        elif user.is_superuser: 
            qs = Prescription.objects.filter(doctor=user)
        else: 
            qs = Prescription.objects.filter(patient=user)

        serializer = PrescriptionSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        if not is_doctor(request.user):
            return Response({"error": "Only doctor"}, status=403)

        appointment = Appointment.objects.filter(doctor=request.user,status="PENDING").order_by("token_number").first()

        presc = Prescription.objects.create(
            appointment=appointment,
            doctor=request.user,
            patient=appointment.patient,
            medications=request.data["medications"],
            portion=request.data["portion"],
            notes=request.data.get("notes", "")
        )

        return Response(PrescriptionSerializer(presc).data)



class BillingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        if is_pharmacist(user):
            qs = Billing.objects.all()
        elif is_patient(user):
            qs = Billing.objects.filter(
                prescription__appointment__patient=user
            )
        elif is_doctor(user):
            qs = Billing.objects.filter(
                prescription__appointment__doctor=user
            )
        else:
            return Response({"error": "Access denied"}, status=403)

        return Response(BillingSerializer(qs, many=True).data)

    def create(self, request):
        if not is_pharmacist(request.user):
            return Response({"error": "Only pharmacist"}, status=403)

        prescription = Prescription.objects.filter(billing__isnull=True).order_by('created_at').first()

        if not prescription:
            return Response({"error": "No prescription pending"}, status=400)

        payment_status = request.data.get("payment_status", "PENDING")

        bill = Billing.objects.create(
            prescription=prescription,
            appointment=prescription.appointment,
            total_amount=request.data.get("total_amount"),
            payment_status=payment_status
        )

        if payment_status == "PAID":
            appointment = prescription.appointment
            appointment.status = "COMPLETED"
            appointment.save()

        return Response(
            BillingSerializer(bill).data,
            status=status.HTTP_201_CREATED
        )



