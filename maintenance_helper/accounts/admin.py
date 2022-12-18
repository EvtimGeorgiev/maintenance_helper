from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

UserAdmin = get_user_model()


@admin.register(UserAdmin)
class AppUserAdmin(auth_admin.UserAdmin):
    pass