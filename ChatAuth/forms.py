from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomAbstractUser

# Updating UserCreationForm to include E-mail field
class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = CustomAbstractUser
        fields = ['username','email','first_name',"last_name",'password1','password2']


