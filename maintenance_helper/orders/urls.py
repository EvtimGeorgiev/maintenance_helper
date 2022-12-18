# orders/urls.py

from django.urls import path


from maintenance_helper.orders.views import OrdersListView, AddToCart, ShowCartView, OrderDetailsView, UpdateCartView

urlpatterns = (
    path('', OrdersListView.as_view(), name='orders list'),
    path('create/', AddToCart.as_view(), name='create oder'),
    # path('<str:pk>/add_to_cart/', AddToCart.as_view(), name='add to cart'),
    path('orders/show_cart/', ShowCartView.as_view(), name='show cart'),
    path('order/<str:pk>/', OrderDetailsView.as_view(), name='order details'),
    path('orders/update_cart/<str:pk>/', UpdateCartView.as_view(), name='update_cart'),
)
