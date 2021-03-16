from datetime import datetime, timedelta, date
from calendar import HTMLCalendar, monthrange
from .models import *

import pandas as pd

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
			self.year = year
			self.month = month
			super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
			events_per_day = events.filter(person__birthday__day=day)
			d = ''
			for event in events_per_day:
					d += f"<li><a href='{event.event_link}'>{event.person.name}'s birthday</li></a>"

			if day != 0:
					return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
			return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
			week = ''
			for d, weekday in theweek:
					week += self.formatday(d, events)
			return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
			events = BirthdayEvent.objects.filter(person__birthday__year=self.year, person__birthday__month=self.month)

			cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
			cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
			cal += f'{self.formatweekheader()}\n'
			for week in self.monthdays2calendar(self.year, self.month):
					cal += f'{self.formatweek(week, events)}\n'
			return cal

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
            # BirthdayEvent.objects.get_or_create(
            #     person=person_existing if person_existing is not None else person_created,
            #     event_link='https://example.com/'
            # )
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
            # BirthdayEvent.objects.get_or_create(
            #     person=person_existing if person_existing is not None else person_created,
            #     event_link='https://example.com/'
            # )

def prev_month(d, today):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    if datetime(prev_month.year, prev_month.month, prev_month.day) <= (today - timedelta(days=366)):
        month = 'month=' + str(first.year) + '-' + str(first.month)
    else:
        month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d, today):
    days_in_month = monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    if datetime(next_month.year, next_month.month, next_month.day) >= (today + timedelta(days=366)):
        month = 'month=' + str(last.year) + '-' + str(last.month)
    else:
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
