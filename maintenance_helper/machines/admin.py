from django.contrib import admin

from maintenance_helper.machines.models import Machine


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    pass
