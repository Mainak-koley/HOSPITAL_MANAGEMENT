from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets +('Profile' , {'fields' : ('username' , 'role' , 'email')})
    fieldsets =  UserAdmin.fieldsets + (
            ('Profile', {'fields':  ('username' , 'role' , 'email')}), # Add your custom field names
        )
    list_display = UserAdmin.list_display + ('username' , 'role' , 'email')