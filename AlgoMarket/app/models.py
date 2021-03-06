from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password
from . import errors
import os

# Create your models here.
class CustomUserManager(BaseUserManager):
    '''
    CustomUserManger used for creating normal users and superusers
    Passwords are stored in hash
    '''
    def create_user(self, email, password, first_name, last_name, username):
        unique_fields = ['email', 'username']
        unique_input = [email, username]
        error = [errors.EmailExist, errors.UsernameExist]
    
        for i in range(len(unique_fields)):
            kwarg = {unique_fields[i]: unique_input[i]}
            try:
                _ = User.objects.get(**kwarg)
                raise error[i]
            except User.DoesNotExist:
                # That particular user with the specified yield don't exists. Fine continue
                pass
        # Safe to add it now, no duplicate user
        toSave = User(email=email, first_name=first_name, last_name=last_name, username=username)
        toSave.password = make_password(password, username + first_name)
        toSave.set_password(raw_password=password)
        toSave.is_active = False
        toSave.save()
        return toSave
        
    def create_superuser(self, username=None, password=None):
        toSave = User(username=username, is_superuser=True, is_staff=True)
        toSave.set_password(raw_password=password)
        toSave.save()

class User(AbstractUser):
    email = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, primary_key=True, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    wallet_address = models.CharField(max_length=200, default='placeholder')
    last_updated = models.TimeField(auto_now=True)
    creator = models.BooleanField(default=False)
    services_completed = models.IntegerField(default=0)
    subscriber_count = models.IntegerField(default=0)
    biography = models.CharField(max_length=1000, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    REQUIRED_FIELDS = []

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    price = models.IntegerField()
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    amount_available = models.IntegerField(default=-1)
    created = models.TimeField(auto_now_add=True)
    last_updated = models.TimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
        
    def imagename(self):
        return os.path.basename(self.image.name)

class Subscription(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pro_price = models.IntegerField(default=0)
    premium_price = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.seller.username} Subscription"

class Perk(models.Model):
    id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    free_amount = models.IntegerField(default=0)
    pro_amount = models.IntegerField(default=0)
    premium_amount = models.IntegerField(default=0)
    
class Transaction(models.Model):
    product = models.ForeignKey(Service, on_delete=models.DO_NOTHING, blank=True, null=True)    
    subscription = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, blank=True, null=True)
    tier = models.CharField(max_length=200, default="Placeholder")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    price = models.IntegerField()
    startDate = models.TimeField(auto_now_add=True)
    fulfillmentDate = models.TimeField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)

class Rating(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    rating = models.IntegerField()
    
    def __str__(self):
        return f"Rating for {self.product.seller.username} Product: {self.product.name}"
    
class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
