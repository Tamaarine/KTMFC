from django import forms
from django.forms import TextInput, EmailField
from app.models import User
from django.contrib import messages

class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, 
                widget=forms.TextInput(attrs={'placeholder': 'Enter your Username', 'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', max_length=150,
                widget=forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=150,
                widget=forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=128,
                widget=forms.TextInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'type': 'password'}))
    confirmed_password = forms.CharField(label='Password', max_length=128,
                widget=forms.TextInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control', 'type': 'password'}))
    email = forms.EmailField(label='Email',
                widget=forms.EmailInput(attrs={'placeholder': 'name@domain.com', 'class': 'form-control'}))
                
    def save(self, request):
        '''
        Create the user from the cleaned form data and save it into the data.
        Return the user object that is created
        '''
        
        if self.cleaned_data['password'] != self.cleaned_data['confirmed_password']:
            print("added")
            messages.error(request, "Password don't match")
            raise forms.ValidationError("Password don't match")
        
        inEmail = self.cleaned_data['email']
        password = self.cleaned_data['password']
        inFirst = self.cleaned_data['first_name']
        inLast = self.cleaned_data['last_name']
        inUsername = self.cleaned_data['username']
        user = User.objects.create_user(inEmail, password, inFirst, inLast, inUsername)
        
        if user is None:
            print("im here")
            messages.error(request, "Same email exists")
            raise forms.ValidationError("Duplicate user")
        else:
            return user 

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                widget=forms.EmailInput(attrs={'placeholder': 'name@domain.com', 'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=128,
                widget=forms.TextInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'type': 'password'}))
                
    