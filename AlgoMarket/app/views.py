from django.shortcuts import render

def index(request):
    context = {
        'nav_bar_name': None,
        'nav_bar_list': [
            {'name': 'Login', 'url': 'login'},
            {'name': 'Register', 'url': 'register'}
        ]
    }
    return render(request, 'app/index.html', context)

def login(request):
    return render(request, 'app/login.html')

def register(request):
    return render(request, 'app/register.html')

def register_creator(request):
    return

def password(request):
    return

def search(request):
    context = {
        'nav_bar_name': None,
        'nav_bar_list': [
            {'name': 'Login', 'url': 'login'},
            {'name': 'Register', 'url': 'register'}
        ],
        'service_card_list': [
            {'name': 'Anime Sketches', 'description': 'I draw beautiful anime sketches for Algorand!', 'image_path': 'yes.jpg'},
            {'name': 'Singing!', 'description': 'I will voice over anything you write for Cryptocurrency', 'image_path': 'sing.jpg'},
            {'name': 'Tax', 'description': 'I do your taxes for crypto', 'image_path': 'accountant.png'},
            {'name': 'Graphic DESIGN!', 'description': 'I will make beautiful graphic design for anything', 'image_path': 'design.jpg'},
            {'name': 'Profession Googler', 'description': 'I am a professional googler and I will google for you', 'image_path': 'google.jpg'}
        ]
    }
    return render(request, 'app/search.html', context)

def store(request):
    return

def creator(request):
    return

def settings(request):
    return

def history(request):
    return

def services(request):
    return

def subscription(request):
    return