from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
)

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('language', 'phone', 'address', 'birthdate', 'gender', 'account_verified'),
        }),
    )

# Register your models here.
# This is a special one
admin.site.register(User, CustomUserAdmin)