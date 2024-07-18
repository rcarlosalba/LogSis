from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'full_name', 'user_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
         'fields': ('full_name', 'address', 'phone', 'user_type')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
         'fields': ('full_name', 'address', 'phone', 'user_type')}),
    )
