from django.shortcuts import render
from rest_framework.response import Response
from .models import User, PatientProfile
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import Userserializer, Patientserializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

def is_doctor(user):
    return user.is_authenticated and user.role == 'role_SU_Doctor'

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role__in=['role_SU_Doctor'])
    serializer_class = Userserializer
    permission_classes = [IsAuthenticated]

    def add_doctor(self, request):
        role = request.data.get('role')

        if role not in ['role_SU_Doctor', 'role_Pharmacist']:
            return Response({"error": "Invalid role. Only 'doctor' or 'pharmacist' allowed."},status=status.HTTP_400_BAD_REQUEST)

        serializer = Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role=role)
            return Response(serializer.data)
        return Response({"message": f" Account created successfully!"}, status=status.HTTP_201_CREATED)
    
    
class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='role_Pharmacist')
    serializer_class = Userserializer
    permission_classes = [IsAuthenticated]


class PatientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='role_Patient')
    serializer_class = Userserializer

    def get_permissions(self):
        if self.action == 'add_patient':
            return [AllowAny()]
        return [IsAuthenticated()]

    def add_patient(self, request):
        serializer = Patientserializer(data=request.data)

        if serializer.is_valid():
            serializer.save(role='patient')
            return Response(serializer.data)
        return Response({"message": "Patient registered successfully!"},status=status.HTTP_201_CREATED)


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = Patientserializer
    permission_classes = [IsAuthenticated]
