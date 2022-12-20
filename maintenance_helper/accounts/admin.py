from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from maintenance_helper.accounts.models import AppUser

UserAdmin = get_user_model()


@admin.register(AppUser)
class AppUserAdmin(auth_admin.UserAdmin):
    pass