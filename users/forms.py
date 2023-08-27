from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['name']
