from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'full_name', 'role', 'is_active', 'created_at')
    search_fields = ('username', 'full_name', 'chat_id')
    list_filter = ('is_active', 'role', 'created_at')
