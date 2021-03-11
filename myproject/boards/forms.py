from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Username'})
    )
    firstname = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'First Name'})
    )
    lastname = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Last Name'})
    )
    email = forms.CharField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Email address'})
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
