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
        ]
    }
    return render(request, 'app/search.html', context)