from django.shortcuts import render

def index(request):
    context = {
        'nav_bar_name': None,
        'nav_bar_list': [
            {'name': 'Login', 'url': '/app/login'},
            {'name': 'Register', 'url': '/app/register'}
        ]
    }
    return render(request, 'app/index.html', context)

def register(request):
    return render(request, 'app/register.html')

def login(request):
    return render(request, 'app/login.html')

def search(request):
    context = {
        'nav_bar_name': None,
        'nav_bar_list': [
            {'name': 'Login', 'url': '/app/login'},
            {'name': 'Register', 'url': '/app/register'}
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