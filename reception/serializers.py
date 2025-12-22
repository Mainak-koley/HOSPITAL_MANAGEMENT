from rest_framework import serializers
from .models import User, PatientProfile, Appointment, Prescription, Billing

class Userserializer(serializers.ModelSerializer): 
    class Meta : 
        model = User 
        fields = "__all__"

class PatientRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.role = 'PATIENT'
        user.save()
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'
        read_only_fields = ['user']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.username",read_only=True)
    class Meta:
        model = Appointment
        fields = ['id','doctor_name','appointment_date','token_number','status','created_at']
        read_only_fields = ['token_number', 'status', 'created_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.username",read_only=True)
    token_number = serializers.IntegerField(source='appointment.token_number',read_only=True)
    patient_name = serializers.CharField(source='patient.username',read_only=True)
    class Meta:
        model = Prescription
        fields = ['id','token_number','doctor_name','patient_name','medications','portion','notes','created_at']
        read_only_fields = ['doctor_name', 'patient_name', 'token_number']


class BillingSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='prescription.appointment.doctor.username',read_only=True)
    patient_name = serializers.CharField(source='prescription.appointment.patient.username',read_only=True)
    token_number = serializers.IntegerField(source='appointment.token_number',read_only=True)
    class Meta:
        model = Billing
        fields = ['token_number','doctor_name','patient_name','total_amount','payment_status']
        read_only_fields = ['token_number','doctor_name','patient_name','payment_status']
