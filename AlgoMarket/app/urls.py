from django.urls import path

from . import requests

urlpatterns = [
    path('', requests.index, name='index'),
    path('login', requests.login, name='login'),
    path('logout', requests.logout, name='logout'),
    path('register', requests.register, name='register'),
    path('register_creator', requests.register_creator, name='register_creator'),
    path('password', requests.password, name='password'),
    path('search', requests.search, name='search'),
    path('store/<int:store_id>', requests.store, name='store'),
    path('profile/<str:username>', requests.profile, name='profile'),
    path('settings', requests.settings, name='settings'),
    path('history', requests.history, name='history'),
    path('services', requests.services, name='services'),
    path('subscription', requests.subscription, name='subscription'),
    path('activate/<str:username>/<str:token>', requests.activate, name='activate'),
    path('report/<str:username>', requests.report, name='report'),
    path('confirmation/<int:transaction_id>', requests.confirmation, name='confirmation')
]