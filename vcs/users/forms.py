from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() #default -> required=true

    class Meta: #nested namspace for configuration
        model =  User #model that will be affected
        fields = ['username', 'email', 'password1', 'password2']

class  UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model =  User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta: #no additional fields
        model = Profile
        fields = ['image']
