import os
import csv
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE','AlgoMarket.settings')

import django
django.setup()

from app.models import User, Service, Subscription

def populate_user():
    with open('sampleUser.csv') as f:
        csv_reader = csv.reader(f)
        next(csv_reader) # Skip header
        # 0,    1     ,     2    ,      3  ,   4  ,    5    
        # id, username, firstname, lastname, email, password
        
        # Try to create user, if exist then just continue
        for line in csv_reader:
            try:
                toAdd = User.objects.create_user(line[4], line[5], line[2], line[3], line[1])
                toAdd.is_active = True
                toAdd.save()
            except:
                pass

def populate_service():
    seed = '1231111'
    random.seed(seed)
    with open('sampleService.csv') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for line in csv_reader:
            try:
                rand = random.randint(0, len(User.objects.all()) - 1)
                service = Service(name=line[0], description=line[1], price=int(line[2]), seller=User.objects.all()[rand])
                service.approved = True
                service.active = True
                service.save()
            except Exception as e:
                print(e)

def populate_subscription():
    _fill = 5 # The number of people to have subscriptions
    for i in range(_fill + 1):
        rand = random.randint(0, len(User.objects.all()) - 1)
        price1 = random.randint(10, 40)
        price2 = random.randint(50, 100)
        subscription = Subscription(seller=User.objects.all()[rand], premium_price=price1, pro_price=price2)        
        subscription.approved = True
        subscription.save()
    

populate_user()
populate_service()
populate_subscription()

super_user = User.objects.create_superuser("a", "123")

        