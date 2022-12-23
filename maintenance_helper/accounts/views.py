# accounts/views.py

from django.contrib.auth import views as auth_views, get_user_model
from django.urls import reverse_lazy
from django.views import generic as views

from maintenance_helper.accounts.forms import UserCreateForm

UserModel = get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login.html'


class RegisterUserView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('index')


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'


class UserEditView(views.UpdateView):
    model = UserModel
    template_name = 'accounts/profile-edit.html'
    fields = ('first_name', 'last_name', 'position', 'image', 'password')

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={
            'pk': self.object.pk,
        })


class UserDeleteView(views.DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('index')


class ManageUsersView(views.ListView):
    model = UserModel
    template_name = 'accounts/manage_users.html'
