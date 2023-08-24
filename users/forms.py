from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SigninForm(UserCreationForm):


    class Meta:
        model = User
        fields = [ 'email', 'username' ]

class LoginForm(AuthenticationForm):
    
    class Meta:
        medel = User
        fields = [ 'email', 'password' ]
