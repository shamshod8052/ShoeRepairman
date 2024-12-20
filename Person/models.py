from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('worker', 'Worker'),
        ('manager', 'Manager'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(_("first name"), max_length=150)
    main_phone = models.CharField(_("Main phone"), max_length=15)
    extra_phone = models.CharField(_("Extra phone"), max_length=15, null=True, blank=True)

    email = None
    EMAIL_FIELD = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return f"{self.get_full_name()}"
