from app.models import User
from django.contrib.auth.backends import ModelBackend

class CustomBackend(ModelBackend):
    def authenticate(self, request, useremail=None, password=None):
        try:
            user = User.objects.get(pk=useremail)
            if user.password == password:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
        
    def get_user(self, useremail):
        try:
            return User.objects.get(pk=useremail)
        except User.DoesNotExist:
            return None