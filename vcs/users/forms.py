from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() #default -> required=true

    class Meta: #nested namspace for configuration
        model =  User #model that will be affected
        fields = ['username', 'email', 'password1', 'password2']
