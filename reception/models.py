from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_ROLE = [
        ('role_super_user' , 'Doctor'), 
        ('role_institute' , 'Medical'), 
        ('role_student' , 'Patient'), 
    ]
    role = models.CharField(max_length=20 , choices=USER_ROLE , default='Student')
    address = models.TextField( null= True , blank= True )
    contact = models.CharField(max_length=12 , null= True , blank= True )