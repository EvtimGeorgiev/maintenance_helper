from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from maintenance_helper.issues.models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):

    list_display = ('pk', 'status', 'short_description', 'created_by', 'created_on', 'closed_on')
    ordering = ('pk',)
    search_fields = ('short_description',)

