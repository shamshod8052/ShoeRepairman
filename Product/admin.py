from django.contrib import admin
from django.db.models import Q, Sum
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter

from .filters import StatusDisplayFilter
from .models import Order, Work, Service, OrderImage, OrderService, RequestOrder, Request


class RequestOrderInline(admin.TabularInline):
    model = RequestOrder
    extra = 0
    verbose_name = _("Order")
    verbose_name_plural = _('Orders')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('customer', 'manager', 'initial_payment', 'created_at')
    search_fields = (
        'initial_payment', 'customer__full_name', 'customer__main_phone', 'customer__extra_phone',
        'manager__first_name', 'manager__last_name', 'manager__main_phone', 'manager__extra_phone'
    )
    list_filter = ('manager', ('created_at', DateRangeFilter))
    inlines = (RequestOrderInline,)

    def save_model(self, request, obj, form, change):
        if not obj.manager:
            obj.manager = request.user
        super().save_model(request, obj, form, change)


class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 0
    verbose_name = _("Service")
    verbose_name_plural = _('Services')


class OrderImageInline(admin.TabularInline):
    model = OrderImage
    extra = 0
    verbose_name = _("Image")
    verbose_name_plural = _('Images')


class WorkInline(admin.TabularInline):
    model = Work
    extra = 0
    verbose_name = _("Works")
    verbose_name_plural = _('Works')
    can_delete = False
    readonly_fields = ['order', 'user', 'status', 'created_at']
    show_change_link = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser or request.user.is_admin or request.user.is_manager:
            return queryset
        return queryset.filter(Q(user=request.user) | Q(for_user_id=request.user.id))


def edit_list(request, list_, field, index=0):
    if not (request.user.is_superuser or request.user.is_admin or request.user.is_manager):
        if field in list_:
            list_.remove(field)
    else:
        if field not in list_:
            list_.insert(index, field)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer', 'status_display', 'total_price_display',
        "qr_code_preview", "get_contract", 'created_at'
    ]
    search_fields = [
        'id', 'description',
        'request_order__request__customer__full_name',
        'request_order__request__customer__main_phone',
        'request_order__request__customer__extra_phone',
        'request_order__request__manager__first_name',
        'request_order__request__manager__last_name',
        'request_order__request__manager__main_phone',
        'request_order__request__manager__extra_phone',
    ]
    list_filter = (StatusDisplayFilter, ('created_at', DateRangeFilter),)
    inlines = (OrderServiceInline, OrderImageInline, WorkInline)

    def customer(self, obj):
        return obj.request_order.request.customer
    customer.short_description = _("Customer")
    customer.admin_order_field = "request_order__request__customer"

    def status_display(self, obj):
        work = obj.last_work
        if not work:
            return Work.Status(Work.Status.NOT_RECEIVED).label
        return Work.Status(work.status).label
    status_display.short_description = "Status"
    status_display.admin_order_field = "request_order__request__customer"

    def get_list_display(self, request):
        edit_list(request, self.list_display, 'customer', 1)
        edit_list(request, self.list_display, 'total_price_display', 2)
        edit_list(request, self.list_display, 'get_contract', -1)

        return self.list_display

    def get_search_fields(self, request):
        edit_list(request, self.search_fields, 'request_order__request__customer__full_name', 0)
        edit_list(request, self.search_fields, 'request_order__request__customer__main_phone', 1)
        edit_list(request, self.search_fields, 'request_order__request__customer__extra_phone', 2)

        return self.search_fields

    def get_contract(self, obj):
        if obj.contract:
            return format_html(
                f'<a href="{obj.contract.url}" download="contract_{obj.id}.pdf">'
                f'{_("Get contract")}'
                f'</a>'
            )
        return _("No contract")
    get_contract.short_description = _("Contract")

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return mark_safe(
                f'<a href="{obj.qr_code.url}" download="qr_code_{obj.id}.png">'
                f'<img src="{obj.qr_code.url}" style="width: 50px; height: 50px;" alt="QR Code" />'
                f'</a>'
            )
        return _("No QR Code")
    qr_code_preview.short_description = _("QR Code")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_price_annotation=Sum('order_services__service__price')
        )

        # if request.user.is_superuser or request.user.is_admin or request.user.is_manager:
        return queryset
        # return queryset.filter(~Q(works=None))

    actions = ['calculate_total_prices']

    def calculate_total_prices(self, request, queryset):
        total_sum = sum(order.total_price for order in queryset)

        if request.user.is_superuser or request.user.is_admin:
            self.message_user(request, _("Total sum of selected orders: {0} UZS").format(total_sum))
        else:
            self.message_user(request, _("You are not an admin."))

    calculate_total_prices.short_description = _("Calculate total price of selected orders")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display')
    search_fields = ('price', 'name', 'description')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('order__id', 'user', 'status', 'created_at')
    search_fields = (
        'user__first_name',
        'user__last_name',
        'order__request_order__request__customer__full_name',
        'user__main_phone',
        'order__request_order__request__customer__main_phone',
        'user__extra_phone',
        'order__request_order__request__customer__extra_phone'
    )
    list_filter = (
        'user',
        'status',
        ('created_at', DateRangeFilter),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser or request.user.is_admin or request.user.is_manager:
            return queryset
        return queryset.filter(Q(user=request.user) | Q(for_user_id=request.user.id))

    def order__id(self, obj):
        return obj.order.id
    order__id.admin_order_field = 'order__id'
    order__id.short_description = 'Order ID'
