from django.urls import path

from maintenance_helper.common.views import index

urlpatterns = (
    path('', index, name='index'),
)
