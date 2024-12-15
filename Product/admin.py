from django.contrib import admin
from django.utils.html import format_html

from .models import Order, Work


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', "qr_code_preview", 'price', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('customer__full_name', 'customer__username')

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                f'<a href="{obj.qr_code.url}" download="qr_code_{obj.id}.png">'
                f'<img src="{obj.qr_code.url}" style="width: 50px; height: 50px;" alt="QR Code" />'
                f'</a>'
            )
        return "No QR Code"

    qr_code_preview.short_description = "QR Code"


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'order', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'start_time', 'end_time')
    search_fields = ('worker__full_name', 'worker__username', 'order__id')
    ordering = ('-start_time',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('worker', 'order')
