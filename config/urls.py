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
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)


urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)