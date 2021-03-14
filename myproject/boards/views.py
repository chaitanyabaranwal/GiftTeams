from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

import pandas as pd

from .forms import *
from .models import *

########################################
############ View functions ############
########################################

# Home view showing all birthdays
@login_required
def home(request):
    events = BirthdayEvent.objects.order_by('person__birthday')
    return render(request, 'birthdaytable.html', {'events': events})

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

# View for showing all members of a team
@login_required
def teams(request):
    teams = Team.objects.filter(hr_person=get_hr_person(request))
    print(teams)
    return render(request, 'team/teams.html', {'teams': teams})

# View for excel upload
@login_required
def upload_excel(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            handle_excel_upload(request, request.FILES['file'])
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UploadExcelForm()
    return render(request, 'upload_excel.html', {'form': form})

# View for viewing members of particular team
@login_required
def view_team(request, team_id=None):
    team = Team.objects.get(id=team_id)
    persons = team.person_set.all()
    return render(request, 'team/view_team.html', {'persons': persons, 'team': team})

# View for creating a new team
@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.hr_person = get_hr_person(request)
            team.save()
            return redirect('teams')
    else:
        form = TeamForm()
    return render(request, 'team/create_team.html', {'form': form})

# View for editing a team
@login_required
def edit_team(request, team_id=None):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('teams')
    else:
        form = TeamForm(instance=team)
    return render(request, 'team/create_team.html', {'form': form})

# View for deleting a team
@login_required
def delete_team(request, team_id=None):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return redirect('teams')

# View for creating a new person
@login_required
def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            # TODO: Update link here
            BirthdayEvent.objects.create(person=person, event_link='https://example.com')
            return redirect('view_team', person.team.id)
    else:
        form = PersonForm()
    return render(request, 'person/create_person.html', {'form': form})

# View for editing a person
@login_required
def edit_person(request, person_id=None):
    person = get_object_or_404(Person, id=person_id)
    team_id = person.team.id
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('view_team', team_id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'person/create_person.html', {'form': form})

# View for deleting a person
@login_required
def delete_person(request, person_id=None):
    person = get_object_or_404(Person, id=person_id)
    team_id = person.team.id
    person.delete()
    return redirect('view_team', team_id)

########################################
########### Helper functions ###########
########################################

# Get HR Person associated with current user
def get_hr_person(request):
    return HRPerson.objects.filter(user=request.user).first()

# Function to handle uploading people from excel sheet
def handle_excel_upload(request, f):
    # Get current user HRPeron
    current_user = get_hr_person(request)
    
    df = pd.read_excel(f)

    for index, row in df.iterrows():
        # Get details
        name = row['Name']
        team = row['Team']
        email = row['Email']
        phone = row['Phone']
        birthday = row['Birthday']

        # Create team if it does not exist
        team_existing, team_created = Team.objects.get_or_create(
            name=team, 
            hr_person=current_user
        )
        team_obj = team_existing if team_existing is not None else team_created

        # Check if support staff
        if team == 'Support':
            person_existing, person_created = Person.objects.get_or_create(
                name=name,
                birthday=birthday,
                email=email,
                phone=phone,
                is_support_person=True,
                team=team_obj,
            )
            # TODO: Fix event link
            BirthdayEvent.objects.get_or_create(
                person=person_existing if person_existing is not None else person_created,
                event_link='https://example.com/'
            )
        # Corporate team member
        else:
            person_existing, person_created = Person.objects.get_or_create(
                name=name,
                birthday=birthday,
                email=email,
                phone=phone,
                is_support_person=False,
                team=team_obj,
            )
            # TODO: Fix event link
            BirthdayEvent.objects.get_or_create(
                person=person_existing if person_existing is not None else person_created,
                event_link='https://example.com/'
            )
