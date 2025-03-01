# MajorHelp/authentication.py

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to authenticate by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If username not found, try email
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        # If the user exists, check the password
        if user.check_password(password):
            return user
        return None
