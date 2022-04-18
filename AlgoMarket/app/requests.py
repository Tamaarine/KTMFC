import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Transaction, User, Service, Subscription, Perk
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.template.loader import render_to_string
from .models import User, Service, Rating, Report
from . import views
from .errors import EmailNotVerified
from .forms import UserLoginForm, UserRegisterForm, CreatorEssayForm, ConfirmTransactionForm, EditUserForm, CreateServiceForm
from .tokenGenerator import token_generator
import json
from . import utils


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
            
            try:
                user = authenticate(request, username=inUsername, password=inPassword)
                if user is not None:
                    auth_login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    messages.error(request, "Username/Password not valid")
            except EmailNotVerified:
                messages.error(request, "Account email is not verified, email verification resent.")
                user = User.objects.get(username=inUsername)
                mail_subject = "Please activate your account"
                html_msg = render_to_string('app/email_template.html', {
                    'username': user.username,
                    'token': token_generator.make_token(user)
                })
                utils.email(mail_subject, user.email, html=html_msg)
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
                html_msg = render_to_string('app/email_template.html', {
                    'username': user.username,
                    'token': token_generator.make_token(user)
                })
                
                to_email = form.cleaned_data['email']
                status_code = utils.email(mail_subject, to_email, html=html_msg)
                
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
        return render(request, 'app/activate_email.html')
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
            form = CreatorEssayForm(request.POST)
            if form.is_valid():
                request.user.biography = form.cleaned_data['essay']
                request.user.save()
                return render(request, 'app/thank_you.html')
            
            
    # User is not logged in please go login to become a creator
    messages.error(request, "Your are not logged in, please log in to register to become a creator!")
    return views.login(request, UserLoginForm())

def password(request):
    return views.password(request)

def search(request):
    return views.search(request)

def store(request, store_id):
    try:
        service = Service.objects.get(pk=store_id)
        return views.store(request, service)
    except Exception as e:
        print(e)
        return HttpResponse("No such store exists")

def profile(request, username):
    return views.profile(request, username)

def settings(request):
    if request.method == "GET":
        initial_input = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }
        if request.user.creator:
            initial_input['biography'] = request.user.biography
        form = EditUserForm(initial=initial_input)
        return views.settings(request, form)
    
    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # save the changes to the form
            form.save()

        return HttpResponseRedirect("/profile/" + str(request.user.username))

def history(request):
    return views.history(request)

def services(request):
    if not request.user.creator:
        return HttpResponse("ONLY CREATORS CAN MANAGE THEIR SERVICES!")

    if request.method == "GET":
        # query the database for services provided by the current user
        return views.services(request)

    if request.method == "POST":
        if not request.POST.get('id', None):
            # create a new Service object in the database based on the form inputs
            form = CreateServiceForm(request.POST, request.FILES)
            if form.is_valid():
                service = form.save(commit=False)
                service.seller = request.user
                service.save()
        else:
            # edit a Service in the database based on the form inputs
            service = Service.objects.get(pk=request.POST['id'])
            if service.seller != request.user:
                return HttpResponse("YOU CANNOT ONLY EDIT SERVICES THAT ARE YOURS!")
            form = CreateServiceForm(request.POST, request.FILES, instance=service)
            if form.is_valid():
                service = form.save(commit=False)
                service.approved = False
                service.active = False
                service.save()
        # then respond with the page with updated list
        return views.services(request)

    if request.method == "PUT":
        # find the appropriate Service object in the database
        data = json.loads(request.body)
        service = Service.objects.get(pk=data['id'])
        if service.seller != request.user:
            return HttpResponse("YOU CANNOT ONLY EDIT SERVICES THAT ARE YOURS!")
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
        # check if current user has a subscription
        try:
            subscription = Subscription.objects.get(pk=request.user)
        except Subscription.DoesNotExist:
            return HttpResponse("CANNOT UPDATE NON-EXISTENT SUBSCRIPTION!")
        # update the perk objects in the database
        Perk.objects.filter(subscription=subscription).delete()
        for id in data['perk_list']:
            # check if the requested service exists and is owned by the current user
            try:
                service = Service.objects.get(pk=id)
                if service.seller != request.user:
                    return HttpResponse("CANNOT ADD A SERVICE THAT YOU DO NOT OWN AS A PERK!")
            except Service.DoesNotExist:
                return HttpResponse("SELECTED SERVICE FOR PERK DOES NOT EXIST!")
            # create the new perk into the database
            perk = Perk(
                subscription = subscription,
                service=service,
                free_amount = data['perk_list'][id]['FreeAmount'],
                pro_amount = data['perk_list'][id]['ProAmount'],
                premium_amount = data['perk_list'][id]['PremiumAmount'],
            )
            perk.save()
        # update the subscription object in the database
        subscription.pro_price = data['pro_price']
        subscription.premium_price = data ['premium_price']
        subscription.approved = False
        subscription.save()
        # then respond with the page with updated subscription
        return views.subscription(request)
      
def report(request, username):

    if request.method == "GET":
        reported_user = User.objects.get(pk=username)
        service_list = Service.objects.filter(seller=reported_user)
        s = []
        for service in service_list:
            s.append(service.name)
        return views.report(request, username, service_list)
    
    if request.method == "POST":
        try:
            form = request.POST
            print("1")
            seller = User.objects.get(pk=username)
            print("2")
            service = Service.objects.filter(seller=seller, name=form.get('service'))
            print("3")
            report = Report(reporter=request.user, service=service[0], description=form.get('description'))
            print("4")
            report.save()
            print("5")
        except:
            return HttpResponse("Sorry, something failed. Please try again later.")

        return HttpResponseRedirect("/profile/" + str(username))

def confirmation(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    if transaction.buyer != request.user:
        return HttpResponse("ONLY BUYERS CAN REVIEW THEIR TRANSACTIONS!")
    if request.method == "POST":
        form = ConfirmTransactionForm(request.POST)
        if form.is_valid():
            # insert adding the review to the DB here
            service = transaction.product
            reviewer = transaction.buyer
            rating = Rating(reviewer=reviewer, product=service, description=form.cleaned_data['review'], rating=form.cleaned_data['rating'])
            rating.save()
            return HttpResponseRedirect("/store/" + str(service.id))
        else:
            return views.confirmation(request, transaction_id, ConfirmTransactionForm())
    elif request.method == "GET":
        print("GETTING")
        return views.confirmation(request, transaction_id, ConfirmTransactionForm())
    return views.confirmation(request, transaction_id, form)
