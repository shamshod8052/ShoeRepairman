from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    ROLE_CHOICES = [
        ('admin', _('Admin')),
        ('worker', _('Worker')),
        ('customer', _('Customer')),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    chat_id = models.BigIntegerField(unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name or self.username or self.chat_id} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
