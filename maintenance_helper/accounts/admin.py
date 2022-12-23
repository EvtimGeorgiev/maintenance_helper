from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from maintenance_helper.accounts.forms import UserCreateForm
from maintenance_helper.accounts.models import AppUser

UserAdmin = get_user_model()


@admin.register(AppUser)
class AppUserAdmin(auth_admin.UserAdmin):
    add_form = UserCreateForm

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                ),
            }),
        (
            'Personal info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                ),
            },
        ),
        (
            'Permissions',
            {
                'fields': (
                    'position',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Important dates',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )