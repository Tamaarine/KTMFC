from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Service
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
import json
from . import views
from .forms import UserLoginForm, UserRegisterForm, CreatorEssayForm


def index(request):
    return views.index(request)

def login(request):
    if request.user.is_authenticated:
        # Already authenticated no reason to go here ever again
        return HttpResponseRedirect('/')
        
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            inUsername = form.cleaned_data['username']
            inPassword = form.cleaned_data['password']
        
            user = authenticate(request, username=inUsername, password=inPassword)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('search')
            else:
                messages.error(request, "Username/Password not valid")
        
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
                # Error handled inside save don't need to do anything
                pass
    elif request.method == "GET":
        return views.register(request, UserRegisterForm())
    return render(request, 'app/register.html', {'form': form})

def register_creator(request):
    if request.user.is_authenticated:
        print("user is authenticated")
        if request.method == "GET":
            # Return the register creator page view
            print("is a get")
            form = CreatorEssayForm()
            return render(request, 'app/register_creator.html', {'form':form})
        elif request.method == "POST":
            # The user submitted the form, time to process it and store it into the
            # database for moderators to view
            print("got here")            
            form = CreatorEssayForm(request.POST)
            if form.is_valid():
                request.user.creator_essay = form.cleaned_data['essay']
                request.user.save()
                return HttpResponse("Essay saved you will hear from us soon!")
            
            
    # User is not logged in please go login to become a creator
    messages.error(request, "Your are not logged in, please log in to register to become a creator!")
    return views.login(request, UserLoginForm())

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
        return HttpResponse("ONLY CREATORS CAN CREATE OR EDIT SERVICES!")

    if request.method == "GET":
        # query the database for services provided by the current user
        service_list = Service.objects.filter(seller=request.user)
        return views.services(request, service_list)

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
        service_list = Service.objects.filter(seller=request.user)
        return views.services(request, service_list)

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
            service_list = Service.objects.filter(seller=request.user)
            return views.services(request, service_list)
        if data['action'] == "toggle-active":
            # change the active status in the database
            service.active = not service.active
            service.save()
            # then respond with a the new page to load
            service_list = Service.objects.filter(seller=request.user)
            return views.services(request, service_list)

def subscription(request):
    return views.subscription(request)
