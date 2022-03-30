from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Service, Subscription, Perk
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from itertools import chain

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
        
    services1 = Service.objects.filter(description__contains=query)
    services2 = Service.objects.filter(name__contains=query)
    query_user = User.objects.filter(username__contains=query)
    services3 = []
    for seller in query_user:
        queried = Service.objects.filter(seller=seller)
        for query in queried:
            services3.append(query)
    total_services = list(chain(services1, services2, services3))
    total_services = set(total_services)
    service_list = []
    for service in total_services:
        service_list.append(service)
    context = {
        'service_list': service_list
    }
    # context['service_list'] = [x for x in context['service_list'] if (q in x['name'] or q in x['description'])]
    return render(request, 'app/search.html', context)

def store(request, context):
    context['service']['image_paths'] = ['search1.PNG', 'search2.PNG', 'search3.PNG', 'search4.PNG']
    context['service']['example_works'] = 'Foo bar, foo bar Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolores dicta veritatis mollitia, voluptates odit similique adipisci rerum in aperiam fugit! Sunt veniam numquam at quisquam officia veritatis, temporibus dicta nemo?'
    context['service']['rating'] = 4.6
    context['service']['rating_count'] = 47
    context['service']['review_count'] = 15
    context['service']['reviews'] = [
        {'author': 'rickylu', 'date': '3 October, 2022', 'rating': 1, 'text': 'Send help, the googler ain\'t googling'},
        {'author': 'daniewu', 'date': '2 October, 2022', 'rating': 5, 'text': 'I came for the service, but stayed for the comments.'},
        {'author': 'robots5252', 'date': '1 October, 2022', 'rating': 5, 'text': 'Two weirdos above me.'}
    ]
    
    return render(request, 'app/store.html', context)

def profile(request):
    service_list = Service.objects.filter(seller=request.user, approved=True, active=True)
    try:
        subscription = Subscription.objects.get(pk=request.user, approved=True)
    except Subscription.DoesNotExist:
        subscription = None
    perk_list = Perk.objects.filter(subscription=subscription)
    context = {
        'service_list': service_list,
        'subscription': subscription,
        'perk_list': perk_list
    }
    return render(request, 'app/profile.html', context)

def settings(request):
    context = {
        'user': {
            'creator': True,
            'username': 'KTMcdonnell',
            'image_path': 'ktm.jpg',
            'first_name': 'Kevin',
            'last_name': 'McDonnell',
            'description': 'I am teaching professor in the Department of Computer Science at Stony Brook University, where I have worked since the summer of 2015. I teach a variety of 100-level and 200-level Computer Science courses.'
        }
    }
    return render(request, 'app/settings.html', context)

def history(request):
    context = {
        'transactions': [
            {'date': '2/27/2022', 'service': 'CSE 101 Tutoring', 'creator': 'KTMcdonnell', 'Price': 50},
            {'date': '1/13/2022', 'service': 'Video Editing', 'creator': 'Rickster99', 'Price': 25},
            {'date': '12/24/2021', 'service': 'Christmas Graphic Design', 'creator': 'SantaClaus1234', 'Price': 25},
            {'date': '7/20/2021', 'service': 'Personal Website Design', 'creator': 'webdevpro1337', 'Price': 100},
            {'date': '2/10/2021', 'service': 'Valentine\'s Song', 'creator': 'SongWriter369', 'Price': 75},
            {'date': '2/9/2021', 'service': 'Valentine\'s Art', 'creator': 'HeartDrawings<3', 'Price': 15}
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
    
def report(request):
    context = {
        'service_list': [
            {'name': 'Anime Sketches', 'description': 'I draw beautiful anime sketches for Algorand!', 'cost': 50, 'image_path': 'yes.jpg'},
            {'name': 'Graphic DESIGN!', 'description': 'I will make beautiful graphic design for anything', 'cost': 75, 'image_path': 'design.jpg'},
            {'name': 'Profession Googler', 'description': 'I am a professional googler and I will google for you', 'cost': 10, 'image_path': 'google.jpg'}
        ],
    }
    return render(request, 'app/report.html', context)
