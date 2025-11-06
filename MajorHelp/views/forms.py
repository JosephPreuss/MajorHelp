# MajorHelp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..discussion_models import ThreadReply
from ..models import DiscussionThread



User = get_user_model()


class NewThreadForm(forms.ModelForm):
    class Meta:
        model = DiscussionThread
        fields = ['category', 'title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Start your discussion...'}),
        }
        
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

class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

class ThreadReplyForm(forms.ModelForm):
    class Meta:
        model = ThreadReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your reply here...',
                'rows': 3,
            }),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def clean_username(self):
        username_or_email = self.cleaned_data['username']
        
        # Check if the input is an email
        if '@' in username_or_email:
            # If it's an email, find the corresponding username
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                raise forms.ValidationError("No user found with this email.")
            return user.username  # Return the username associated with the email
        
        # If it's not an email, treat it as a username
        return username_or_email
    
    