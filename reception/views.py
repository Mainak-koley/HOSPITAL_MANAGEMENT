from django.shortcuts import render
from rest_framework.response import Response
from .models import DoctorProfile, User, PatientProfile
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import DoctorSerializer, PatientSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status

class Doctorviewset(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def reg_doctor(self, request):
        register = DoctorProfile(request.data)

        if register.is_valid():
            register.save()
            return Response(register.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def token(self, request):
        token = request.data.get('verify_token')
        VALID_TOKENS = ['DOC1234567', 'HOSP9876543', 'VERIFY00001']

        if token not in VALID_TOKENS:
            return Response({'error': 'Invalid hospital token'}, status=status.HTTP_400_BAD_REQUEST)
        

class Patientviewset(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def reg_doctor(self, request):
        register = PatientProfile(request.data)

        if register.is_valid():
            register.save()
            return Response(register.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class PharmacistLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = IsAuthenticated(username=username, password=password)

        if user and user.role == 'Pharmacist':
            return Response({'message': 'Pharmacist login successful', 'username': user.username})
        return Response({'error': 'Invalid credentials or not a pharmacist'}, status=status.HTTP_401_UNAUTHORIZED)