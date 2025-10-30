from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_ROLE = [
        ('role_SU_Doctor' , 'Doctor'), 
        ('role_Pharmacist' , 'Pharmacist'), 
        ('role_Patient' , 'Patient'), 
    ]
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20 , choices=USER_ROLE , default='role_Patient')
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.role == 'role_SU_Doctor':
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username