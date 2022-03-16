from app.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

class CustomBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None):
        '''
        Since we are implementing our own custom backend authentication instead of using the default
        Django one. I have to use username as parameter instead of email. This is because the admin page
        sends the email and password using the name of 'username' and 'password' instead of 'email' and 'password'
        Which result in bad match when it is checking method signature. It will skip our backend authentication
        and doesn't uses it. 
        '''
        try:
            user = User.objects.get(pk=username)
            if check_password(password, user.password):
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