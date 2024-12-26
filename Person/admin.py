from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter

from Person.models import CustomUser, Customer
from Product.models import Work, Request


class WorkInline(admin.TabularInline):
    model = Work
    extra = 0
    verbose_name = _("Works")
    verbose_name_plural = _('Works')
    can_delete = False
    readonly_fields = ['work_', 'order', 'user', 'status', 'created_at']
    show_change_link = False

    def work_(self, work):
        url = f"/admin/Product/work/?id__exact={work.id}"
        return format_html(
            f"<a href='{url}'>{work.id}</a>"
        )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class RequestInline(admin.TabularInline):
    model = Request
    extra = 0
    verbose_name = _("Request")
    verbose_name_plural = _('Requests')
    can_delete = False
    readonly_fields = ('request_', 'customer', 'manager', 'initial_payment', 'created_at')
    show_change_link = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def request_(self, request):
        url = f"/admin/Product/request/?id__exact={request.id}"

        return format_html(
            f"<a href='{url}'>{request.id}</a>"
        )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('main_phone', 'password', 'first_name', 'last_name', 'extra_phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',), 'fields': (
                    'main_phone', 'password1', 'password2', 'first_name', 'last_name', 'extra_phone',
                    'is_active', 'is_staff', 'groups'
                ),
            },
        ),
    )
    list_display = ('main_phone', 'get_full_name', 'is_staff', 'is_active')
    list_filter = ('groups', 'is_staff', 'is_active')
    search_fields = ('main_phone', 'first_name', 'last_name', 'extra_phone')
    ordering = ()
    inlines = (RequestInline, WorkInline)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser or request.user.is_admin:
            return queryset
        return queryset.filter(main_phone=request.user.main_phone)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'main_phone', 'extra_phone')
    list_filter = (('created_at', DateRangeFilter),)
    search_fields = ('full_name', 'main_phone', 'extra_phone')
    inlines = (RequestInline,)
