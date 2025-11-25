from django.db import models
from django.utils.translation import gettext_lazy as _


class Request(models.Model):
    customer = models.ForeignKey(
        'Person.Customer',
        verbose_name=_('Customer'),
        on_delete=models.CASCADE,
        related_name='requests',
    )
    manager = models.ForeignKey(
        'Person.CustomUser',
        verbose_name=_('Manager'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='request_managers',
        editable=False,
    )
    initial_payment = models.DecimalField(
        verbose_name=_('Initial payment(UZS)'),
        max_digits=10, decimal_places=0,
        default=0,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return self.customer.get_full_name()

    class Meta:
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')


class RequestOrder(models.Model):
    request = models.ForeignKey(
        Request,
        verbose_name=_('Request'),
        on_delete=models.CASCADE,
        related_name='request_orders',
    )
    order = models.OneToOneField(
        'Order',
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name='request_order'
    )

    def __str__(self):
        return f"{self.request}"

    class Meta:
        verbose_name = _('Request order')
        verbose_name_plural = _('Request orders')


class Order(models.Model):
    description = models.TextField(_("Description"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    submission_time = models.DateTimeField(_("Submission time"), null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True, editable=False)
    contract = models.FileField(upload_to='contracts/', null=True, blank=True, editable=False)

    @property
    def last_work(self):
        work = None
        if self.works.exists():
            work = self.works.order_by('-id').first()

        return work

    @property
    def one_before_last_work(self):
        work = None
        if self.works.count() >= 2:
            work = self.works.order_by('-id').all()[1]

        return work

    @property
    def status(self):
        return self.works.filter(status=Work.Status.APPROVED).exists()

    @property
    def total_price(self):
        if self.order_services.exists():
            return sum([s.service.price for s in self.order_services.all()])
        return 0

    def total_price_display(self):
        if self.order_services.exists():
            return f"{self.total_price} UZS"
        return 0
    total_price_display.short_description = _("Total Price")
    total_price_display.admin_order_field = 'total_price_annotation'

    @property
    def received_user(self):
        work = self.works.filter(status=Work.Status.NOT_RECEIVED).order_by('-created_at').first()
        return work.user if work else None

    @property
    def done_user(self):
        work = self.works.filter(status=Work.Status.DONE).order_by('-created_at').first()
        return work.user if work else None

    @property
    def rejected_user(self):
        work = self.works.filter(status=Work.Status.REJECTED).order_by('-created_at').first()
        return work.user if work else None

    @property
    def approved_user(self):
        work = self.works.filter(status=Work.Status.APPROVED).order_by('-created_at').first()
        return work.user if work else None

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    price = models.DecimalField(
        verbose_name=_('Price(UZS)'),
        max_digits=10, decimal_places=0,
        default=0,
    )
    description = models.TextField(_('Description'), null=True, blank=True)

    def price_display(self):
        return f"{self.price}"
    price_display.short_description = _("Price")
    price_display.admin_order_field = "price"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class OrderService(models.Model):
    order = models.ForeignKey(
        'Order',
        verbose_name=_('Order'),
        on_delete=models.CASCADE,
        related_name='order_services'
    )
    service = models.ForeignKey(
        Service,
        verbose_name=_("Service"),
        on_delete=models.CASCADE,
        related_name='order_services'
    )

    def __str__(self):
        return f"{self.order}"

    class Meta:
        verbose_name = _("Order service")
        verbose_name_plural = _("Order services")
        unique_together = ('order', 'service')


class OrderImage(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_('Order'),
        on_delete=models.CASCADE,
        related_name='order_images'
    )
    photo = models.ImageField(_("Photo"), upload_to='photos/')

    def __str__(self):
        return f"{self.order}"

    class Meta:
        verbose_name = _("Order image")
        verbose_name_plural = _("Order images")


class Work(models.Model):
    class Status(models.IntegerChoices):
        NOT_RECEIVED = 0, _("✉️ Not received")
        IN_PROCESS = 1, _("🕒 In process")
        DONE = 2, _("🗸 Done")
        REJECTED = 3, _("❗️ Rejected")
        APPROVED = 4, _("✔️ Approved")

    order = models.ForeignKey(
        'Order',
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name='works'
    )
    user = models.ForeignKey(
        'Person.CustomUser',
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name='works',
        limit_choices_to={'is_active': True},
    )
    for_user_id = models.IntegerField(
        verbose_name=_("For user"),
        null=True,
        editable=False,
    )
    status = models.IntegerField(
        _("Status"),
        choices=Status.choices,
        default=Status.NOT_RECEIVED,
        editable=False
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.order.id}"

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")
