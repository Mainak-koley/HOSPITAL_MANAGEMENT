from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PatientProfile, Appointment, Prescription, Billing


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Profile', {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Profile', {'fields': ('role',)}),)
    list_display = ('username','email','first_name','last_name','role','is_staff','is_superuser','is_active',)

    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(PatientProfile)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Billing)
