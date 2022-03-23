from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Service
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
import json
from . import views


def index(request):
    return views.index(request)

def login(request):
    if request.user.is_authenticated:
        # Already authenticated no reason to go here ever again
        return HttpResponseRedirect('/')
        
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("NOT A VALID USER!")
        
    elif request.method == "GET":
        return views.login(request)

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
        inEmail = request.POST.get('email')
        inPassword = request.POST.get('password')
        inFirst = request.POST.get('firstname')
        inLast = request.POST.get('lastname')
        inUsername = request.POST.get('username')
        user = User.objects.create_user(inEmail, inPassword, inFirst, inLast, inUsername)
        auth_login(request, user)
        messages.success(request, "Registration successful." )
        return HttpResponseRedirect('/')

    elif request.method == "GET":
        # User is just getting the registeration html, just sent it
        return views.register(request)

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
