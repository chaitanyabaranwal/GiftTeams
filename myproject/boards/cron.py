from .models import BirthdayEvent, Person
from .utils import create_birthday

from datetime import datetime, timedelta, date

# Function to remove all the birthday events from previous years
def remove_old_birthdays():
    now = date.today()
    before = now - timedelta(days=366)
    BirthdayEvent.objects.filter(date < before).delete()

# Function to add all the birthday events from now to next year
def add_new_birthdays():
    # Iterate through all birthdays and create birthday events in the next year
    persons = Person.objects.all()
    for person in persons:
        create_birthday(person)
