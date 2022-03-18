from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import datetime
from django.contrib.auth.hashers import make_password


# Create your models here.
class CustomUserManager(BaseUserManager):
    '''
    CustomUserManger used for creating normal users and superusers
    Passwords are stored in hash
    '''
    def create_user(self, email, password, first_name, last_name, username):
        toSave = User(email=email, first_name=first_name, last_name=last_name, username=username)
        toSave.password = make_password(password, username + first_name)
        toSave.set_password(raw_password=password)
        toSave.save()
        return toSave
    def create_superuser(self, email, password, username=None):
        toSave = User(email=email, is_superuser=True, is_staff=True)
        toSave.set_password(raw_password=password)
        toSave.save()

class User(AbstractUser):
    email = models.CharField(max_length=200, primary_key=True)
    walletAddress = models.CharField(max_length=200)
    last_updateed = models.TimeField(auto_now=True)
    creator = models.BooleanField(default=False)
    service_completed = models.IntegerField(default=0)
    subscriber_count = models.IntegerField(default=0)
    bio = models.CharField(max_length=200)
    last_login = models.TimeField(default=datetime.datetime.now())
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Service(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    amount_available = models.IntegerField()
    created = models.TimeField(auto_now_add=True)
    last_updated = models.TimeField(auto_now=True)
    imagePath = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    
class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Service, on_delete=models.CASCADE)    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    startDate = models.TimeField()
    fulfillmentDate = models.TimeField()

class Rating(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    rating = models.IntegerField()
    