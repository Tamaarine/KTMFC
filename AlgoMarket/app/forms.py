from django import forms
from django.forms import TextInput, EmailField, Textarea
from app.models import User, Service
from django.contrib import messages
from django.core.validators import MaxValueValidator, MinValueValidator
from .errors import *

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
        
        # If it passes all the field checks then user will be created and returned
        try:
            user = User.objects.create_user(inEmail, password, inFirst, inLast, inUsername)
        except UsernameExist:
            messages.error(request, "Same username exists")
        except EmailExist:
            messages.error(request, "Same email exists")
        
        return user 

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username',
                widget=forms.TextInput(attrs={'placeholder': 'Enter your Username', 'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=128,
                widget=forms.TextInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'type': 'password'}))
                
class CreatorEssayForm(forms.Form):
    essay = forms.CharField(max_length=1000, 
                widget=forms.Textarea(attrs={'placeholder': 'Share your work experience, projects, or area of expertise', 'class': 'form-control is-invalid', 'type': 'password'}))

class ConfirmTransactionForm(forms.Form):
    confirm = forms.BooleanField(label="Confirm")
    rating = forms.IntegerField(label="Rating", required=False,
                validators=[MaxValueValidator(5), MinValueValidator(1)])
    review = forms.CharField(max_length=300, required=False,
                widget=forms.Textarea(attrs={'placeholder': 'Write your review here', 'class': 'form-control'}))

class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description', 'price', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.TextInput(attrs={'class': 'form-control'})
        }