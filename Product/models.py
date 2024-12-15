from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Order(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, _('Pending')
        IN_PROGRESS = 2, _('In Progress')
        COMPLETED = 3, _('Completed')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        'Admin.User',
        on_delete=models.CASCADE,
        related_name='orders',
        limit_choices_to={'role': 'customer'}
    )
    shoe_image = models.ImageField(upload_to='shoes/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3,
                                choices=[('USD', 'USD'), ('UZS', 'UZS'), ('EUR', 'EUR')],
                                default='UZS')
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True, editable=False)
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.full_name} - {self.get_status_display()}"


class Work(models.Model):
    class Status(models.IntegerChoices):
        STARTED = 1, _('Started')
        IN_PROGRESS = 2, _('In Progress')
        COMPLETED = 3, _('Completed')

    worker = models.ForeignKey(
        'Admin.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'worker'},
        related_name='works'
    )
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='work'
    )
    status = models.IntegerField(choices=Status.choices, default=Status.STARTED)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    # worker and order and status == "InProgress" be unique

    def __str__(self):
        return f"Work on Order {self.order.id} by {self.worker.full_name or self.worker.username}"

    class Meta:
        verbose_name = "Work"
        verbose_name_plural = "Works"
