from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    first_name = forms.CharField(label='First Name', max_length=150)
    last_name = forms.CharField(label='Last Name', max_length=150)
    password = forms.CharField(label='Password', max_length=128)
    confirmed_password = forms.CharField(label='Password', max_length=128)