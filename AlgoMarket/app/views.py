from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        context = {
            'navbar': {
                'name': request.user.username,
                'list': [
                    {'name': 'Profile', 'url': 'profile'},
                    {'name': 'Logout', 'url': 'logout'}
                ]
            }
        }
    else:
        context = {
            'navbar': {
                'name': None,
                'list': [
                    {'name': 'Login', 'url': 'login'},
                    {'name': 'Register', 'url': 'register'}
                ]
            }
        }
    return render(request, 'app/index.html', context)

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
        return render(request, 'app/login.html')

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return render(request, 'app/index.html')
    else:
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
        return render(request, 'app/register.html')

def register_creator(request):
    return render(request, 'app/register_creator.html')

def password(request):
    return render(request, 'app/password.html')

def search(request):
    context = {
        'navbar': {
            'name': None,
            'list': [
                {'name': 'Login', 'url': 'login'},
                {'name': 'Register', 'url': 'register'}
            ]
        },
        'service_list': [
            {'name': 'Anime Sketches', 'description': 'I draw beautiful anime sketches for Algorand!', 'image_path': 'yes.jpg'},
            {'name': 'Singing!', 'description': 'I will voice over anything you write for Cryptocurrency', 'image_path': 'sing.jpg'},
            {'name': 'Tax', 'description': 'I do your taxes for crypto', 'image_path': 'accountant.png'},
            {'name': 'Graphic DESIGN!', 'description': 'I will make beautiful graphic design for anything', 'image_path': 'design.jpg'},
            {'name': 'Profession Googler', 'description': 'I am a professional googler and I will google for you', 'image_path': 'google.jpg'}
        ]
    }
    return render(request, 'app/search.html', context)

def store(request):
    context = {
        'navbar': {
            'name': None,
            'list': [
                {'name': 'Login', 'url': 'login'},
                {'name': 'Register', 'url': 'register'}
            ]
        },
        'service': {
            'name': 'Profession Googler',
            'image_paths': ['search1.PNG', 'search2.PNG', 'search3.PNG', 'search4.PNG'],
            'description': 'This is a simple description of my humble store, while it has nothing in the beginning I will let you know that in the near furture this will become the next Facebook of the century, mark my word it will come true. By then I will become a millionaire and laughing while sitting at my throne while you are at your petty little chair writing "code".',
            'example_works': 'Foo bar, foo bar Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolores dicta veritatis mollitia, voluptates odit similique adipisci rerum in aperiam fugit! Sunt veniam numquam at quisquam officia veritatis, temporibus dicta nemo?',
            'email': 'nowhere@mozilla.org',
            'cost': 69.42,
            'subscription_costs': [0, 10, 20],
            'rating': 4.6,
            'rating_count': 46,
            'review_count': 15,
            'reviews': [
                {'author': 'rickylu', 'date': '3 October, 2022', 'rating': 1, 'text': 'Send help, the googler ain\'t googling'},
                {'author': 'daniewu', 'date': '2 October, 2022', 'rating': 5, 'text': 'I came for the service, but stayed for the comments.'},
                {'author': 'robots5252', 'date': '1 October, 2022', 'rating': 5, 'text': 'Two weirdos above me.'}
            ]
        }
    }
    return render(request, 'app/store.html', context)

def profile(request):
    context = {
        'user': {
            'creator': True,
            'username': 'KTMcdonnell',
            'email': 'ktm@cs.stonybrook.edu',
            'image_path': 'ktm.jpg',
            'first_name': 'Kevin',
            'last_name': 'McDonnell',
            'services_completed': 37,
            'subscriber_count': 3,
            'rating': 5,
            'description': 'I am teaching professor in the Department of Computer Science at Stony Brook University, where I have worked since the summer of 2015. I teach a variety of 100-level and 200-level Computer Science courses.'
        },
        'service_list': [
            {'name': 'Anime Sketches', 'description': 'I draw beautiful anime sketches for Algorand!', 'image_path': 'yes.jpg'},
            {'name': 'Graphic DESIGN!', 'description': 'I will make beautiful graphic design for anything', 'image_path': 'design.jpg'},
            {'name': 'Profession Googler', 'description': 'I am a professional googler and I will google for you', 'image_path': 'google.jpg'}
        ],
        'subscription': {
            'perks': ['homework questions', 'google searches', 'tutoring sessions', 'code reviews'],
            'free': {'cost': 0, 'quantities': [1,1,0,0]},
            'pro': {'cost': 50, 'quantities': [5,5,1,0]},
            'premium': {'cost': 100, 'quantities': ['unlimited','unlimited',4,1]}
        }
    }
    return render(request, 'app/profile.html', context)

def settings(request):
    context = {
        'navbar': {
            'name': 'KTMcdonnell',
            'list': [
                {'name': 'My Profile', 'url': 'profile'},
                {'name': 'Settings', 'url': 'settings'},
                {'name': 'My Services', 'url': 'services'},
                {'name': 'My Subscription', 'url': 'subscription'},
                {'name': 'History', 'url': 'history'},
                {'name': 'Logout', 'url': 'index'}
            ]
        },
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
        'navbar': {
            'name': 'KTMcdonnell',
            'list': [
                {'name': 'My Profile', 'url': 'profile'},
                {'name': 'Settings', 'url': 'settings'},
                {'name': 'My Services', 'url': 'services'},
                {'name': 'My Subscription', 'url': 'subscription'},
                {'name': 'History', 'url': 'history'},
                {'name': 'Logout', 'url': 'index'}
            ]
        },
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
    context = {
        'navbar': {
            'name': 'KTMcdonnell',
            'list': [
                {'name': 'My Profile', 'url': 'profile'},
                {'name': 'Settings', 'url': 'settings'},
                {'name': 'My Services', 'url': 'services'},
                {'name': 'My Subscription', 'url': 'subscription'},
                {'name': 'History', 'url': 'history'},
                {'name': 'Logout', 'url': 'index'}
            ]
        },
        'service_list': [
            {'name': 'Anime Sketches', 'description': 'I draw beautiful anime sketches for Algorand!', 'cost': 50, 'image_path': 'yes.jpg'},
            {'name': 'Graphic DESIGN!', 'description': 'I will make beautiful graphic design for anything', 'cost': 75, 'image_path': 'design.jpg'},
            {'name': 'Profession Googler', 'description': 'I am a professional googler and I will google for you', 'cost': 10, 'image_path': 'google.jpg'}
        ]
    }
    return render(request, 'app/manage_services.html', context)

def subscription(request):
    context = {
        'navbar': {
            'name': 'KTMcdonnell',
            'list': [
                {'name': 'My Profile', 'url': 'profile'},
                {'name': 'Settings', 'url': 'settings'},
                {'name': 'My Services', 'url': 'services'},
                {'name': 'My Subscription', 'url': 'subscription'},
                {'name': 'History', 'url': 'history'},
                {'name': 'Logout', 'url': 'index'}
            ]
        },
        'service_list': [
            {'name': 'Anime Sketches', 'description': 'I draw beautiful anime sketches for Algorand!', 'cost': 50, 'image_path': 'yes.jpg'},
            {'name': 'Graphic DESIGN!', 'description': 'I will make beautiful graphic design for anything', 'cost': 75, 'image_path': 'design.jpg'},
            {'name': 'Profession Googler', 'description': 'I am a professional googler and I will google for you', 'cost': 10, 'image_path': 'google.jpg'}
        ],
        'subscription': {
            'perks': ['homework questions', 'google searches', 'tutoring sessions', 'code reviews'],
            'free': {'cost': 0, 'quantities': [1,1,0,0]},
            'pro': {'cost': 50, 'quantities': [5,5,1,0]},
            'premium': {'cost': 100, 'quantities': ['unlimited','unlimited',4,1]}
        }
    }
    return render(request, 'app/manage_subscription.html', context)
    
def viewmodel(request):
    # return HttpResponse("hello world")
    response = ""
    for user in User.objects.all():
        response += f"<H1>Email: {user.email} Bio: {user.bio} Username: {user.username} Password: {user.password}</H1>"
    
    return HttpResponse(response)