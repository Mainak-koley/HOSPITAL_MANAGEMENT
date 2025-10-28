from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.
class User(AbstractUser, PermissionsMixin):
    USER_ROLE = [
        ('role_SU_Doctor' , 'Doctor'), 
        ('role_Pharmacist' , 'Pharmacist'), 
        ('role_Patient' , 'Patient'), 
    ]
    role = models.CharField(max_length=20 , choices=USER_ROLE , default='role_Patient')

    def save(self, *args, **kwargs):
        if self.role == 'role_SU_Doctor':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)
    
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=100)
    specialist_in = models.CharField(max_length=100)
    lab_no = models.CharField(max_length=50)
    verify_token = models.CharField(max_length=10)
    token = models.CharField(max_length=10, unique=True)
    used = models.BooleanField(default=False)

def __str__(self):
    return self.name

class PatientProfile(models.Model):
    createdAt = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
