# accounts/forms.py

from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'bio', 'profile_picture']