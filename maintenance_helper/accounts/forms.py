from maintenance_helper.core.mixins import PlaceholderMixin
from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class UserCreateForm(PlaceholderMixin, auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('position', 'username', 'first_name', 'last_name', 'email', 'password1')
        field_classes = {"username": auth_forms.UsernameField}

    def clean_title(self):
        return self.cleaned_data['username'].capitalize()



