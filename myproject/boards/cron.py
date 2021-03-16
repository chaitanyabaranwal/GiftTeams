from .models import BirthdayEvent, Person

from datetime import datetime, timedelta, date

# Function to remove all the birthday events from previous years
def remove_old_birthdays():
    now = date.today()
    before = now - timedelta(days=366)
    BirthdayEvent.objects.filter(date < before).delete()

# Function to add all the birthday events from now to next year
def add_new_birthdays():
    persons = Person.objects.all()
    print(map(lambda x: x.birthday, persons))

add_new_birthdays()
