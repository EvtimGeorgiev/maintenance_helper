from django.urls import path

from maintenance_helper.common.views import index, access_denied

urlpatterns = (
    path('', index, name='index'),
    path('access_denied', access_denied, name='access denied'),
)
