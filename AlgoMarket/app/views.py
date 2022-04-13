from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User, Service, Subscription, Perk, Rating, Transaction
from .forms import CreateServiceForm
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

def store(request, service):
    try:
        # get the subscription costs
        subs = Subscription.objects.filter(seller=service.seller)
        if len(subs) > 0:
            sub_costs = [0, subs[0].pro_price, subs[0].premium_price]
        else:
            sub_costs = None
        # get the rating information
        ratings = Rating.objects.filter(product=service)
        avg_rating = 0
        if len(ratings) > 0:
            for rating in ratings:
                avg_rating += rating.rating
            avg_rating /= len(ratings)
        # get the perk information
        perk = Perk.objects.filter(service=service)
        perk_amount = []
        if len(perk) > 0:
            perk = perk[0]
            perk_amount = [perk.free_amount, perk.pro_amount, perk.premium_amount]
        else:
            # User did not make any perk amount for this particualr service
            sub_costs = None
    except Exception as e:
        print(e)
        return HttpResponse("Sorry, something failed. Please check back later")

    context = {'service':{'name':service.name, 
        # 'image_paths':service.image_path,
        'description':service.description,
        'seller_username': service.seller.username,
        'email': service.seller.email,
        'cost': service.price,
        'subscription_costs': sub_costs,
        'perk_amount': perk_amount,
        'rating': avg_rating,
        'review_count': len(ratings),
        'reviews': ratings,
        'id': service.id
        }}
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
    all_transactions = Transaction.objects.filter(buyer=request.user)
    transactions = [trans for trans in all_transactions if trans.product]
    subscriptions = [trans for trans in all_transactions if trans.subscription]
    context = {
        'transactions': transactions,
        'subscriptions': subscriptions
    }
    return render(request, 'app/history.html', context)

def services(request):
    service_list = Service.objects.filter(seller=request.user)
    context = {
        'service_list': service_list,
        'create_form': CreateServiceForm()
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
