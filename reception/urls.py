from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, AppointmentViewSet, PatientProfileViewSet, PrescriptionViewSet, BillingViewSet

router = DefaultRouter()
router.register('register_patient', AuthViewSet, basename='auth')
router.register('patientprofile', PatientProfileViewSet, basename='patientprofile')
router.register('appointments', AppointmentViewSet, basename='appointment')
router.register('prescriptions', PrescriptionViewSet, basename='prescription')
router.register('billing', BillingViewSet, basename='billing')

urlpatterns = []

urlpatterns += router.urls
