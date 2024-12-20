from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Order, Work, Service, OrderImage, OrderService


class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 0
    verbose_name_plural = _('Services')
    verbose_name = _("Service")


class OrderImageInline(admin.TabularInline):
    model = OrderImage
    extra = 0
    verbose_name_plural = _('Photos')
    verbose_name = _("Photo")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status_display', 'total_price_display', 'received_time', 'submission_time', "qr_code_preview", "get_contract")
    search_fields = ('customer__username', 'customer__first_name', 'customer__last_name', 'customer__main_phone', 'customer__extra_phone', 'description')
    list_filter = ('received_time', 'submission_time')
    inlines = (OrderServiceInline, OrderImageInline)

    def status_display(self, obj):
        work = obj.works.order_by('-status').first()
        if not work:
            return Work.Status(0).label
        return Work.Status(work.status).label

    status_display.short_description = "Status"

    def get_contract(self, obj):
        if obj.contract:
            return format_html(
                f'<a href="{obj.contract.url}" download="contract_{obj.id}.pdf">'
                f'{_("Get contract")}'
                f'</a>'
            )
        return _("No contract")

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return mark_safe(
                f'<a href="{obj.qr_code.url}" download="qr_code_{obj.id}.png">'
                f'<img src="{obj.qr_code.url}" style="width: 50px; height: 50px;" alt="QR Code" />'
                f'</a><br>'
                f'<a href="javascript:void(0);" onclick="window.open(\'{obj.qr_code.url}\', \'_blank\').print();">'
                f'{_("Print")}</a>'
            )
        return _("No QR Code")

    qr_code_preview.short_description = _("QR Code")
    get_contract.short_description = _("Contract")
    Order.total_price_display.fget.short_description = _("Total Price")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display')
    search_fields = ('price', 'name', 'description')
    list_filter = ('currency',)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('worker', 'order__id', 'status', 'received_time', 'submission_time', 'approve_time')
    search_fields = ('worker__full_name', 'order__customer__full_name',
                     'worker__phone', 'order__customer__phone')
    list_filter = ('status', 'received_time', 'submission_time')
