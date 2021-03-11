from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import SignUpForm
from .models import HRPerson

# Create your views here.
def home(request):
    return HttpResponse('Hello, world!')

# View for user signin
def signin(request):
    return render(request, 'index.html')

# View for user signup
def signup(request):
    # If data is submitted by user
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            person = HRPerson(user=user)
            person.save()
            return HttpResponseRedirect('/home/')
    # If user visits the page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def birthdaytable(request):
    return render(request, 'birthdaytable.html')
