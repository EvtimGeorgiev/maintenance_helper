from django.contrib import admin

from maintenance_helper.orders.models import Order, OrderedItem, Cart


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
