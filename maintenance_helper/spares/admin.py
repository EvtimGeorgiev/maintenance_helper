from django.contrib import admin

from maintenance_helper.spares.models import SparePart, Stock


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass
