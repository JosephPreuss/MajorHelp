# MajorHelp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Add any fields you want to customize here
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    # Optionally, you can override the clean() method to remove certain validations
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # You can add your own password validation here if neede
        return password1
