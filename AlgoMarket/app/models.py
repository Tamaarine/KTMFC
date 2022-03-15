from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=200, primary_key=True)
    username = models.CharField(max_length=200)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    walletAddress = models.CharField(max_length=200)
    created = models.TimeField(auto_now_add=True)
    last_updateed = models.TimeField(auto_now=True)
    service_completed = models.IntegerField()
    subscriber_count = models.IntegerField()
    bio = models.CharField(max_length=200)
    last_login = models.TimeField(default=datetime.datetime.now())
    
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
    