from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Doctorviewset, Patientviewset, PharmacistLoginView

router = DefaultRouter()
router.register('doctor/register', Doctorviewset, basename='doctor-register')
router.register('patient/register', Patientviewset, basename='patient-register')

urlpatterns = [
    path('pharmacist/login/', PharmacistLoginView.as_view(), name='pharmacist-login'),
]

urlpatterns+=router.urls