from django.urls import path, include

from maintenance_helper.accounts.views import SignInView, RegisterUserView, SignOutView, \
    UserDetailsView, UserEditView, UserDeleteView, ManageUsersView

urlpatterns = (
    path('login/', SignInView.as_view(), name='login user'),
    path('manage_users/', ManageUsersView.as_view(), name='manage users'),
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='details user'),
        path('edit/', UserEditView.as_view(), name='edit user'),
        path('delete/', UserDeleteView.as_view(), name='delete user'),
    ])),
)
