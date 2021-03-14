from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import FileExtensionValidator

from .models import *

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Username'})
    )
    first_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
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

class SignInForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class UploadExcelForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls', 'csv'])])

class TeamForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Team name'})
    )
    class Meta:
        model = Team
        fields = ('name',)

class PersonForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Name'})
    )
    email = forms.CharField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Email address'})
    )
    phone = forms.CharField(
        label='',
        widget=forms.NumberInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Phone'})
    )
    birthday = forms.DateField(
        label='',
        widget=forms.DateInput(attrs={'class': 'mb-3 form-control', 'placeholder': 'Birthday'})
    )
    team = forms.ModelChoiceField(
        label='Select Team',
        queryset=Team.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'mb-3 form-control', 'placeholder': 'Team'})
    )
    class Meta:
        model = Person
        fields = ('name', 'email', 'phone', 'birthday', 'team')
