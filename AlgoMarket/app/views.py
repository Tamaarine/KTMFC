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
    return render(request, 'app/register_creator.html')

def password(request):
    return render(request, 'app/password.html')

def search(request):
    context = {
        'nav_bar_name': None,
        'nav_bar_list': [
            {'name': 'Login', 'url': 'login'},
            {'name': 'Register', 'url': 'register'}
        ],
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
        'nav_bar_name': None,
        'nav_bar_list': [
            {'name': 'Login', 'url': 'login'},
            {'name': 'Register', 'url': 'register'}
        ],
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