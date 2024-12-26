from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUser(AbstractUser):
    main_phone = models.CharField(_("Phone number"), max_length=15, unique=True)
    first_name = models.CharField(_("First name"), max_length=150)
    last_name = models.CharField(_("Last name"), max_length=150)
    extra_phone = models.CharField(_("Extra phone"), max_length=15, null=True, blank=True)
    username = models.CharField(_("username"), max_length=150, null=True, blank=True, editable=False)

    USERNAME_FIELD = "main_phone"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_admin(self):
        return self.groups.filter(name__in=['Admin']).exists()

    @property
    def is_manager(self):
        return self.groups.filter(name__in=['Manager']).exists()

    @property
    def is_worker(self):
        return self.groups.filter(name__in=['Worker']).exists()

    def __str__(self):
        return f"{self.get_full_name()}"


class Customer(models.Model):
    full_name = models.CharField(_("Fullname"), max_length=255, null=True)
    main_phone = models.CharField(_("Main phone"), max_length=20)
    extra_phone = models.CharField(_("Extra phone"), max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return (f"{self.full_name} "
                f"{self.main_phone[-4:] if self.main_phone else self.extra_phone[-4:] if self.extra_phone else ''}")

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        unique_together = ("full_name", "main_phone")
