from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Service, Subscription, Perk
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def index(request):
    return render(request, 'app/index.html')

def login(request, form):
    return render(request, 'app/login.html', {'form':form})

def register(request, form):
    return render(request, 'app/register.html', {'form': form})

def register_creator(request, form):
    return render(request, 'app/register_creator.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return render(request, 'app/index.html')
    else:
        return HttpResponseRedirect('index')
    
def password(request):
    return render(request, 'app/password.html')

def search(request):
    query = request.GET.get('sch')
    
    if query is None:
        return render(request, 'app/index.html',)
        
    services = Service.objects.filter(description__contains=request.GET.get('sch'))
    service_list = []
    for service in services:
        service_list.append(service)
    context = {
        'service_list': service_list
    }
    # context['service_list'] = [x for x in context['service_list'] if (q in x['name'] or q in x['description'])]
    return render(request, 'app/search.html', context)

def store(request, service):
    # TODO make sure to change the reviews stuff to retrieve them and update values in the context accordingly
    # TODO same with subscription costs
    context = {'service':{'name':service.name, 
        'image_paths':service.image_path,
        'description':service.description,
        'seller_username': service.seller.username,
        'email': service.seller.email,
        'cost': service.price,
        'subscription_costs': [0, 10, 20],
        'rating': 4.6,
        'rating_count': 46,
        'review_count': 15,
        'reviews': [
            {'author': 'rickylu', 'date': '3 October, 2022', 'rating': 1, 'text': 'Send help, the googler ain\'t googling'},
            {'author': 'daniewu', 'date': '2 October, 2022', 'rating': 5, 'text': 'I came for the service, but stayed for the comments.'},
            {'author': 'robots5252', 'date': '1 October, 2022', 'rating': 5, 'text': 'Two weirdos above me.'}
        ]}}
    return render(request, 'app/store.html', context)

def profile(request, username):
    service_list = Service.objects.filter(seller=request.user, approved=True, active=True)
    try:
        subscription = Subscription.objects.get(pk=request.user, approved=True)
    except Subscription.DoesNotExist:
        subscription = None
    perk_list = Perk.objects.filter(subscription=subscription)
    context = {
        'selected_user': User.objects.get(pk=username),
        'service_list': service_list,
        'subscription': subscription,
        'perk_list': perk_list
    }
    return render(request, 'app/profile.html', context)

def settings(request, form):
    return render(request, 'app/settings.html', {'form':form})

def history(request):
    context = {
        'transactions': [
            {'date': '2/27/2022', 'service': 'CSE 101 Tutoring', 'creator': 'KTMcdonnell', 'Price': 50, 'id': 1},
            {'date': '1/13/2022', 'service': 'Video Editing', 'creator': 'Rickster99', 'Price': 25, 'id': 2},
            {'date': '12/24/2021', 'service': 'Christmas Graphic Design', 'creator': 'SantaClaus1234', 'Price': 25, 'id': 3},
            {'date': '7/20/2021', 'service': 'Personal Website Design', 'creator': 'webdevpro1337', 'Price': 100, 'id': 4},
            {'date': '2/10/2021', 'service': 'Valentine\'s Song', 'creator': 'SongWriter369', 'Price': 75, 'id': 5},
            {'date': '2/9/2021', 'service': 'Valentine\'s Art', 'creator': 'HeartDrawings<3', 'Price': 15, 'id': 6}
        ],
        'subscriptions': [
            {'creator': 'KTMcdonnell', 'tier': 'Premium', 'cost': 100, 'status': 'Active'},
            {'creator': 'Rickster99', 'tier': 'Free', 'cost': 0, 'status': 'Active'},
            {'creator': 'WhaleLover42', 'tier': 'Pro', 'cost': 10, 'status': 'Inactive'}
        ]
    }
    return render(request, 'app/history.html', context)

def services(request):
    service_list = Service.objects.filter(seller=request.user)
    context = {
        'service_list': service_list
    }
    return render(request, 'app/manage_services.html', context)

def subscription(request):
    try:
        subscription = Subscription.objects.get(pk=request.user)
    except Subscription.DoesNotExist:
        subscription = None
    service_list = Service.objects.filter(seller=request.user, approved=True, active=True)
    perk_list = Perk.objects.filter(subscription=subscription)
    context = {
        'subscription': subscription,
        'service_list': service_list,
        'perk_list': perk_list
    }
    return render(request, 'app/manage_subscription.html', context)
    
def report(request, username, service_list):
    s_list = []
    for service in service_list:
        s_list.append(service.name)
    context = {
        'username': username,
        'service_list': s_list
    }
    return render(request, 'app/report.html', context)

def confirmation(request, transaction_id, form):
    context = {'transaction_id': transaction_id, 'form': form}
    return render(request, 'app/confirmation.html', context)
