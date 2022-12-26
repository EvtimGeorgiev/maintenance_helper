from django.contrib.auth import get_user_model
from django.shortcuts import redirect

UserModel = get_user_model()


class PlaceholderMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, _ in self.fields.items():
            field = self.fields.get(field_name)
            field.widget.attrs.update({'placeholder': field.label})


class TechnicianAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.position == 'operator':
            return redirect('access denied')
        return super().dispatch(request, *args, **kwargs)


class MaintenanceAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.position in ('operator', 'technician'):
            return redirect('access denied')
        return super().dispatch(request, *args, **kwargs)


class ManagerAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.position in ('operator', 'technician', 'maintenance'):
            return redirect('access denied')
        return super().dispatch(request, *args, **kwargs)


class MaintenanceOnlyAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.position not in ('maintenance', 'admin'):
            return redirect('access denied')
        return super().dispatch(request, *args, **kwargs)


class ManagerOnlyAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.position not in ('manager', 'admin'):
            return redirect('access denied')
        return super().dispatch(request, *args, **kwargs)


class AdminOnlyAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.position != 'admin':
            return redirect('access denied')
        return super().dispatch(request, *args, **kwargs)
