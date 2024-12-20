from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type', 'main_phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'main_phone', 'extra_phone'),
        }),
    )
    list_display = ('username', 'get_full_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'main_phone', 'extra_phone')

admin.site.register(CustomUser, CustomUserAdmin)
