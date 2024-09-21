from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ['email']
    
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'is_superuser', 'auth_provider']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff', 'is_superuser']

    # Customizing fieldsets to match your User model
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        (_('Authentication Provider'), {'fields': ('auth_provider',)}),
    )
    
    # Make created_at and last_login read-only fields
    readonly_fields = ['created_at', 'last_login']

    # Fields to display when creating a new user in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
