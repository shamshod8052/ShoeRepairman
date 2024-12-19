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
    list_display = ('id', 'customer', 'status_display', 'total_price_display', 'start_time', 'finish_time', "qr_code_preview", "get_contract")
    search_fields = ('customer__full_name', 'customer__phone', 'customer__extra_phone', 'description')
    list_filter = ('start_time', 'finish_time')
    inlines = (OrderServiceInline, OrderImageInline)

    def status_display(self, obj):
        if obj.status:
            return format_html(f'<span style="color: green; font-weight: bold;">{_("✔ Done")}</span>')
        else:
            return format_html(f'<span style="color: red; font-weight: bold;">{_("✘ Pending")}</span>')

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
                f'Print</a>'
            )
        return "No QR Code"

    qr_code_preview.short_description = "QR Code"
    get_contract.short_description = _("Contract")
    Order.total_price_display.fget.short_description = _("Total Price")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display')
    search_fields = ('price', 'name', 'description')
    list_filter = ('currency',)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('worker', 'order__id', 'status', 'start_time', 'finish_time', 'approve_time')
    search_fields = ('worker__full_name', 'order__customer__full_name',
                     'worker__phone', 'order__customer__phone')
    list_filter = ('status', 'start_time', 'finish_time')
