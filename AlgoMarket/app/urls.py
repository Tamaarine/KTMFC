from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('register_creator', views.register_creator, name='register_creator'),
    path('password', views.password, name='password'),
    path('search', views.search, name='search'),
    path('store', views.store, name='store'),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('history', views.history, name='history'),
    path('services', views.services, name='services'),
    path('subscription', views.subscription, name='subscription'),
    path('test', views.viewmodel, name='testing')
]