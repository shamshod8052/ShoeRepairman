from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    full_name = models.CharField(_("Fullname"), max_length=100, null=True)
    phone = models.CharField(_("Main phone"), max_length=20)
    extra_phone = models.CharField(_("Extra phone"), max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return (f"{self.full_name} "
                f"{self.phone[-4:] if self.phone else self.extra_phone[-4:] if self.extra_phone else ''}")

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class Worker(models.Model):
    full_name = models.CharField(_("Fullname"), max_length=100, null=True)
    phone = models.CharField(_("Phone"), max_length=20)
    extra_phone = models.CharField(_("Extra phone"), max_length=20, null=True, blank=True)
    is_active = models.BooleanField(_("Is active"), default=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return (f"{self.full_name} "
                f"{self.phone[-4:] if self.phone else self.extra_phone[-4:] if self.extra_phone else ''}")

    class Meta:
        verbose_name = _("Worker")
        verbose_name_plural = _("Workers")
