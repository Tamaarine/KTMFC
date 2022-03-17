from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password, make_password
from . import views


def index(request):
    return views.index(request)

def login(request):
    if request.user.is_authenticated:
        # Already authenticated no reason to go here ever again
        return HttpResponseRedirect('search')
        
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('search')
        else:
            return HttpResponse("NOT A VALID USER!")
        
    elif request.method == "GET":
        return views.login(request)

def logout(request):
    return views.logout(request)
    
def register(request):
    if request.method == "POST":
        # Making a post request we will handle it
        print(request.POST.get('password'))
        
        return HttpResponse("THIS IS A POST REQUEST!")
    elif request.method == "GET":
        # User is just getting the registeration html, just sent it
        return views.register()

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
    return views.services(request)

def subscription(request):
    return views.services(request)
    
def report(request):
    return views.report(request)
