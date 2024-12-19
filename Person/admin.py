from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from Person.models import Customer, Worker


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "extra_phone", "orders", "created_at")
    search_fields = ("full_name", "phone", "extra_phone")
    list_filter = ("created_at",)

    def orders(self, obj):
        url = f"/admin/Product/order/?customer_id__exact={obj.id}&q="
        n = obj.orders.count()
        return format_html(f'<a href="{url}">{_("View Orders")}({n})</a>')

    orders.short_description = _("View orders")


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "extra_phone", "created_at")
    search_fields = ("full_name", "phone", "extra_phone")
    list_filter = ("created_at",)
