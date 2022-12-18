# spares\urls.py

from django.urls import path, include

from maintenance_helper.spares.views import SparePartsListView, SparePartCreateView, SparePartsDetailView, \
    SparePartEditView, SparePartDeleteView, StockItemsView, StockItemEdit

urlpatterns = (
    path('', SparePartsListView.as_view(), name='spare parts'),
    path('create/', SparePartCreateView.as_view(), name='part create'),
    path('<str:pk>/details/', SparePartsDetailView.as_view(), name='part details'),
    path('<str:pk>/edit/', SparePartEditView.as_view(), name='part edit'),
    path('<str:pk>/delete/', SparePartDeleteView.as_view(), name='part delete'),

    path('stock/', include([
        path('', StockItemsView.as_view(), name='stock list'),
        path('<str:pk>/edit_item/', StockItemEdit.as_view(), name='edit stock item'),
    ])),

)

from .signals import *
