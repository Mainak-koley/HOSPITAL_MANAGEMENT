from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, PharmacistViewSet, PatientViewSet, PatientProfileViewSet

router = DefaultRouter()
router.register('doctor/register', DoctorViewSet, basename='doctor')
router.register('pharmacists', PharmacistViewSet, basename='pharmacist')
router.register('patient/register', PatientViewSet, basename='patient')
router.register('patientprofiles', PatientProfileViewSet, basename='patientprofile')

urlpatterns = [
]

urlpatterns+=router.urls