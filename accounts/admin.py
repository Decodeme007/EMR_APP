from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Institution, User


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'subscription_tier', 'is_active', 'created_at')
    search_fields = ('name', 'code')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'institution', 'is_staff')
    list_filter = ('role', 'institution', 'is_staff', 'is_superuser')
    # Edit existing user
    fieldsets = UserAdmin.fieldsets + (
        (
            'Clinic & Role Info',
            {
                'fields': (
                    'institution',
                    'role',
                    'phone',
                    'profile_picture',
                )
            }
        ),
    )

    # Add new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Clinic & Role Info',
            {
                'fields': (
                    'institution',
                    'role',
                    'phone',
                    'profile_picture',
                )
            }
        ),
    )