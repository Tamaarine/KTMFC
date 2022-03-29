from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.template.loader import render_to_string
from .models import User, Service
from . import views
from .errors import EmailNotVerified
from .forms import UserLoginForm, UserRegisterForm, CreatorEssayForm
from .tokenGenerator import token_generator
import json
from . import utils


def index(request):
    # send_mail("kill yourself", "please kiss me", 'algomarket@algomarket.com', ['irebootplaygt@gmail.com'])
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
            
            try:
                user = authenticate(request, username=inUsername, password=inPassword)
                if user is not None:
                    auth_login(request, user)
                    return HttpResponseRedirect('search')
                else:
                    messages.error(request, "Username/Password not valid")
            except EmailNotVerified:
                messages.error(request, "Account email is not verified")
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
                
                mail_subject = "Please activate your account"
                message = render_to_string('app/email_template.html', {
                    'username': user.username,
                    'token': token_generator.make_token(user)
                })
                
                to_email = form.cleaned_data['email']
                status_code = utils.email(mail_subject, message, to_email)
                
                if status_code == 200:
                    messages.success(request, 'Please check your email for account verification')
                else:
                    messages.error(request, "Server side error")
                
                return render(request, 'app/register.html', {'form': UserRegisterForm()})
            except Exception as e:
                # Error handled inside save don't need to do anything
                print(e)
                pass
    elif request.method == "GET":
        return views.register(request, UserRegisterForm())
    return render(request, 'app/register.html', {'form': form})

def activate(request, username, token):
    try:
        user = User.objects.get(pk=username)
    except User.DoesNotExist:
        user = None
    
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thank you for verifying your email!")
    elif user.is_active:
        return HttpResponse("User is already activated!")
    else:
        return HttpResponse("Invalid activation link!")

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

def report(request):
    return views.report(request)
