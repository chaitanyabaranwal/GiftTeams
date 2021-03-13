from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import SignUpForm, SignInForm, UploadExcelForm
from .models import HRPerson

# Create your views here.
def home(request):
    return render(request, 'birthdaytable.html')

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

# View for excel upload
def upload_excel(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            print('Excel file submitted!')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UploadExcelForm()
    return render(request, 'upload_excel.html', {'form': form})
