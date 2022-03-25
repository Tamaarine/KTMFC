from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Service, Subscription, Perk
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
import json
from . import views
from .forms import UserLoginForm, UserRegisterForm


def index(request):
    return views.index(request)

def login(request):
    if request.user.is_authenticated:
        # Already authenticated no reason to go here ever again
        return HttpResponseRedirect('/')
        
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            inEmail = form.cleaned_data['email']
            inPassword = form.cleaned_data['password']
        
            user = authenticate(request, username=inEmail, password=inPassword)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('search')
            else:
                messages.error(request, "Email/Password not valid")
        
    elif request.method == "GET":
        return views.login(request, UserLoginForm())
    return render(request, 'app/login.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return HttpResponseRedirect('/')
    
def register(request):
    if request.user.is_authenticated:
        # Already authenticated no reason to go here ever again
        return HttpResponseRedirect('search')
    
    if request.method == "POST":
        # Making a post request we will handle it
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(request)            
                auth_login(request, user)
                return HttpResponseRedirect('/')
            except:
                pass
    elif request.method == "GET":
        return views.register(request, UserRegisterForm())
    return render(request, 'app/register.html', {'form': form})

def register_creator(request):
    return views.register_creator(request)

def password(request):
    return views.password(request)

def search(request):
    return views.search(request)

def store(request):
    return views.store(request)

def profile(request):
    return views.profile(request)

def settings(request):
    return views.settings(request)

def history(request):
    return views.history(request)

def services(request):
    if not request.user.creator:
        return HttpResponse("ONLY CREATORS CAN MANAGE THEIR SERVICES!")

    if request.method == "GET":
        # query the database for services provided by the current user
        return views.services(request)

    if request.method == "POST":
        # create a new Service object in the database
        data = json.loads(request.body)
        service = Service(
            id=Service.objects.count(),
            name=data['name'],
            seller=request.user,
            description=data['description'],
            price=data['price'],
            amount_available=-1
        )
        service.save()
        messages.success(request, "Service creation successful." )
        # then respond with the page with updated list
        return views.services(request)

    if request.method == "PUT":
        # find the appropriate Service object in the database
        data = json.loads(request.body)
        service = Service.objects.get(pk=data['id'])
        if service.seller != request.user:
            return HttpResponse("YOU CANNOT ONLY EDIT SERVICES THAT ARE YOURS!")
        if data['action'] == "update-service":
            # update the service in the database
            service.name = data['name']
            service.description = data['description']
            service.price = data['price']
            service.approved = False
            service.active = False
            service.save()
            messages.success(request, "Service update was successful." )
            # then respond with a the new page to load
            return views.services(request)
        if data['action'] == "toggle-active":
            # change the active status in the database
            service.active = not service.active
            service.save()
            # then respond with a the new page to load
            return views.services(request)

def subscription(request):
    if not request.user.creator:
        return HttpResponse("ONLY CREATORS CAN MANAGE THEIR SUBSCRIPTION!")

    if request.method == "GET":
        # attempt to find the current user's subscription
        return views.subscription(request)

    if request.method == "POST":
        # check for existing subscription by user
        try:
            subscription = Subscription.objects.get(pk=request.user)
            return HttpResponse("CREATOR CANNOT CREATE MULTIPLE SUBSCRIPTIONS!")
        except Subscription.DoesNotExist:
            pass
        # create a new Subscription object in the database
        subscription = Subscription(
            seller=request.user
        )
        subscription.save()
        messages.success(request, "Subscription creation successful." )
        # then respond with the page with updated subscription
        return views.subscription(request)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data['action'] == 'add-perk':
            # check if current user has a subscription
            try:
                subscription = Subscription.objects.get(pk=request.user)
            except Subscription.DoesNotExist:
                return HttpResponse("CANNOT ADD A PERK TO NON-EXISTENT SUBSCRIPTION!")
            # check if the requested service exists and is owned by the current user
            try:
                service = Service.objects.get(pk=data['service_id'])
                if service.seller != request.user:
                    return HttpResponse("CANNOT ADD A SERVICE THAT YOU DO NOT OWN AS A PERK!")
            except Service.DoesNotExist:
                return HttpResponse("SELECTED SERVICE FOR PERK DOES NOT EXIST!")
            # create a new Perk in the database for current user's subscription
            perk = Perk(
                id=Perk.objects.count(),
                subscription=subscription,
                service=service
            )
            perk.save()
            messages.success(request, "Perk creation successful." )
            # then respond with the page with updated subscription
            return views.subscription(request)
