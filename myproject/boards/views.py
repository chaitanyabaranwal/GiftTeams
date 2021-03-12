from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import SignUpForm, SignInForm
from .models import HRPerson

# Create your views here.
def home(request):
    return render(request, 'birthdaytable.html')

# View for user signin
def signin(request):
    # If data is submitted by user
    if request.method == 'POST':
        form = SignInForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # Valid user
        if user is not None:
            login(request, user)
            return redirect('home')
    # If user visits the page
    else:
        form = SignInForm()
    return render(request, 'signin/signin.html', {'form': form})

# View for user signup
def signup(request):
    # If data is submitted by user
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            person = HRPerson.objects.create(user=form.save())
            login(request, person.user)
            return redirect('home')
    # If user visits the page
    else:
        form = SignUpForm()
    return render(request, 'signin/signup.html', {'form': form})
