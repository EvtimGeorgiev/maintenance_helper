from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('maintenance_helper.common.urls')),
    path('accounts/', include('maintenance_helper.accounts.urls')),
    path('machines/', include('maintenance_helper.machines.urls')),
    path('issues/', include('maintenance_helper.issues.urls')),
    path('spares/', include('maintenance_helper.spares.urls')),
    path('orders/', include('maintenance_helper.orders.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
