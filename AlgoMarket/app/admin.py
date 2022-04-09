from django.contrib import admin
from .models import User, Service, Transaction, Rating, Subscription, Perk, Report, ActiveSubscription

# Register your models here.
admin.site.register(User)
admin.site.register(Service)
admin.site.register(Subscription)
admin.site.register(Perk)
admin.site.register(Transaction)
admin.site.register(Rating)
admin.site.register(Report)
admin.site.register(ActiveSubscription)