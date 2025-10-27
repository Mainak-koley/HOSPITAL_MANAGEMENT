from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.
class User(AbstractUser, PermissionsMixin):
    USER_ROLE = [
        ('role_SU_Doctor' , 'Doctor'), 
        ('role_Pharmacist' , 'Pharmacist'), 
        ('role_Patient' , 'Patient'), 
    ]
    role = models.CharField(max_length=20 , choices=USER_ROLE , default='Patient')
    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False)
    
