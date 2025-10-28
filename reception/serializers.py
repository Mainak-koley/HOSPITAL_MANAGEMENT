from rest_framework import serializers
from .models import User, DoctorProfile, PatientProfile

class DoctorSerializer(serializers.ModelSerializer):
    class Meta : 
        model = DoctorProfile
        fields = "__all__"

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"
