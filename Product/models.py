from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Work(models.Model):
    class Status(models.IntegerChoices):
        NOT_RECEIVED = 0, _("❌ Not Received")
        RECEIVED = 1, _("🕒 Received")
        UNAPPROVED = 2, _("⚠️ Unapproved")
        APPROVED = 3, _("✔️ Approved")

    order = models.ForeignKey(
        'Order',
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name='works'
    )
    worker = models.ForeignKey(
        'Person.Worker',
        verbose_name=_("Worker"),
        on_delete=models.CASCADE,
        related_name='works',
        limit_choices_to={'is_active': True},
    )
    status = models.IntegerField(
        _("Status"),
        choices=Status.choices,
        default=Status.NOT_RECEIVED,
        editable=False
    )
    start_time = models.DateTimeField(_("Start time"), auto_now_add=True)
    finish_time = models.DateTimeField(_("Finish time"), null=True, blank=True, editable=False)
    approve_time = models.DateTimeField(_("Approve time"), null=True, blank=True, editable=False)

    def received(self):
        self.status = self.Status.RECEIVED
        self.save()

    def finished(self):
        self.finish_time = timezone.now()
        self.status = self.Status.UNAPPROVED
        self.save()

    @property
    def is_finished(self):
        return self.status in [self.Status.UNAPPROVED, self.Status.APPROVED]

    def approved(self):
        self.approve_time = timezone.now()
        self.status = self.Status.APPROVED
        self.save()

    def __str__(self):
        return f"{self.worker.full_name} - {self.order.id}"

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    price = models.PositiveIntegerField(_('Price'))
    currency = models.CharField(_("Currency"), max_length=3,
                                choices=[('UZS', 'UZS')],
                                default='UZS')
    description = models.TextField(_('Description'), null=True, blank=True)

    @property
    def price_display(self):
        return f"{self.price} {self.currency}"

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency}"

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class Order(models.Model):
    customer = models.ForeignKey(
        'Person.Customer',
        verbose_name=_('Customer'),
        on_delete=models.CASCADE,
        related_name='orders'
    )
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True, editable=False)
    contract = models.FileField(upload_to='contracts/', null=True, blank=True, editable=False)
    description = models.TextField(_("Description"), null=True, blank=True)
    start_time = models.DateTimeField(_("Start time"), default=timezone.now)
    finish_time = models.DateTimeField(_("Finish time"))

    @property
    def status(self):
        if self.works.filter(status=Work.Status.APPROVED).exists():
            return True
        return False

    @property
    def total_price(self):
        if self.order_services.exists():
            return sum([s.service.price for s in self.order_services.all()])
        return 0

    @property
    def total_price_display(self):
        if self.order_services.exists():
            return f"{self.total_price} {self.order_services.first().service.currency}"
        return 0

    def __str__(self):
        return f"{self.customer.full_name}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderService(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_('Order'),
        on_delete=models.CASCADE,
        related_name='order_services'
    )
    service = models.ForeignKey(Service, verbose_name=_("Service"),
                                on_delete=models.CASCADE,
                                related_name='order_services')

    def __str__(self):
        return f"{self.order.customer.full_name}"

    class Meta:
        verbose_name = _("OrderImage")
        verbose_name_plural = _("OrderImages")
        unique_together = ('order', 'service')


class OrderImage(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_('Order'),
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.ImageField(_("Photo"), upload_to='photos/')

    def __str__(self):
        return f"{self.order.customer.full_name}"

    class Meta:
        verbose_name = _("OrderImage")
        verbose_name_plural = _("OrderImages")
