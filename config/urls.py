from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve

from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('success_order/<int:order_id>/', views.success_order, name='success_order'),
    path('approve_work/<int:order_id>/', views.approve_work, name='approve_work'),
    path('reject_work/<int:order_id>/', views.reject_work, name='reject_work'),
    path('', admin.site.urls),
)


urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)