from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), 
        ('A-', 'A-'),
        ('B+', 'B+'), 
        ('B-', 'B-'),
        ('AB+', 'AB+'), 
        ('AB-', 'AB-'),
        ('O+', 'O+'), 
        ('O-', 'O-'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    dob = models.DateField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS = (
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField(default=timezone.now)
    token_number = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'appointment_date', 'token_number')
        ordering = ['token_number']

    def __str__(self):
        return f"{self.token_number} - {self.patient.username}"


class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescriptions')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescriptions')
    medications = models.JSONField()
    portion = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.username} by {self.doctor.username}"


class Billing(models.Model):
    STATUS = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    prescription = models.OneToOneField(Prescription, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=STATUS, default='PENDING')

    def __str__(self):
        return f"Billing {self.id} - {self.appointment.patient.username} - {self.payment_status}"
