from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import datetime

# Create your models here.
class CustomUserManager(BaseUserManager):
    '''
    CustomUserManger used for creating normal users and superusers
    Passwords are stored in hash
    '''
    def create_user(self, email, password, username=None):
        toSave = User(email=email)
        toSave.set_password(raw_password=password)
        toSave.save()
    def create_superuser(self, email, password, username=None):
        toSave = User(email=email, is_superuser=True, is_staff=True)
        toSave.set_password(raw_password=password)
        toSave.save()

class User(AbstractUser):
    email = models.CharField(max_length=200, primary_key=True)
    username = models.CharField(max_length=200)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    walletAddress = models.CharField(max_length=200)
    created = models.TimeField(auto_now_add=True)
    last_updateed = models.TimeField(auto_now=True)
    service_completed = models.IntegerField(default=0)
    subscriber_count = models.IntegerField(default=0)
    bio = models.CharField(max_length=200)
    last_login = models.TimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Service(models.Model):
    id = models.IntegerField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    amount_available = models.IntegerField()
    created = models.TimeField(auto_now_add=True)
    last_updateed = models.TimeField(auto_now=True)
    imagePath = models.CharField(max_length=200)
    renewalRate = models.IntegerField()
    activate = models.BooleanField(default=False)
    
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
    
class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
