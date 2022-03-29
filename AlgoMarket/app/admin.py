from django.contrib import admin
from .models import User, Service, Transaction, Rating, Report

# Register your models here.
admin.site.register(User)
admin.site.register(Service)
admin.site.register(Transaction)
admin.site.register(Rating)
admin.site.register(Report)
