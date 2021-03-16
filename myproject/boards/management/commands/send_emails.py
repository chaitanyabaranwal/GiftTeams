from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, send_mass_mail
from boards.models import BirthdayEvent, Person
from myproject.settings import EMAIL_HOST_USER as EMAIL_ADDR
import datetime

INVITE_DAYS_BEFORE = 7
REMINDER_DAYS_BEFORE = 7

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        """
        We send out scheduled emails on three cases:
        1. One week before birthday to friends.
        2. One day before birthday to friends.
        3. On the birthday to the person.
        """
        self.handle_invites()
        self.handle_reminders()
        self.handle_on_birthday()

    def handle_invites(self):
        """
        We fetch birthday events that will happen in INVITE_DAYS_BEFORE
        days and send emails.
        """
        birthday_date = (datetime.date.today()
                         + datetime.timedelta(days=INVITE_DAYS_BEFORE))
        birthday_people = (Person.objects
                           .filter(birthday__day=birthday_date.day)
                           .filter(birthday__month=birthday_date.month))
        for person in birthday_people:
            friends = get_friends(person)
            friends_emails = [f.email for f in friends]
            event = BirthdayEvent.objects.get(person=person)
            assert(person not in friends)
            self.send_invite_email(person.name, event.event_link, friends_emails)

    def handle_reminders(self):
        """
        We fetch birthday events that will happen in REMINDER_DAYS_BEFORE
        and send emails.
        """
        birthday_date = (datetime.date.today()
                         + datetime.timedelta(days=REMINDER_DAYS_BEFORE))
        birthday_people = (Person.objects
                           .filter(birthday__day=birthday_date.day)
                           .filter(birthday__month=birthday_date.month))
        for person in birthday_people:
            friends = get_friends(person)
            friends_emails = [f.email for f in friends]
            event = BirthdayEvent.objects.get(person=person)
            assert(person not in friends)
            self.send_reminder_email(person.name, event.event_link, friends_emails)
        pass

    def get_friends(self, person):
        friends = (Person.objects
                    .exclude(name__exact=person.name))
        # if not a support staff then just inform the person's team
        if not person.is_support_person:
            friends = friends.filter(team__exact=person.team)
        return friends

    def handle_on_birthday(self):
        today = datetime.date.today() + datetime.timedelta(days=REMINDER_DAYS_BEFORE)
        birthday_people = (Person.objects
                           .filter(birthday__day=today.day)
                           .filter(birthday__month=today.month))
        for person in birthday_people:
            event = BirthdayEvent.objects.get(person=person)
            age = today.year - person.birthday.year
            self.send_celebrate_email(person.name, event.event_link, person.email)

    def send_invite_email(self, birthday_person, birthday_link, recipient_list):
        send_mail(f"{birthday_person}'s birthday",
                  f"{birthday_person} birthday liao give money pls thx {birthday_link}",
                  EMAIL_ADDR,
                  recipient_list)
        # ['tanyeejian@gmail.com']) # you can put your email here to test

    def send_reminder_email(self, birthday_person, birthday_link, recipient_list):
        send_mail(f"Last Reminder: {birthday_person}'s birthday",
                  f"{birthday_person} birthday tmr give money pls thx {birthday_link}",
                  EMAIL_ADDR,
                  recipient_list)
        # ['tanyeejian@gmail.com']) # you can put your email here to test

    def send_celebrate_email(self, birthday_person, birthday_link, recipient_email):
        send_mail(f"Happy Birthday {birthday_person}!",
                  ("Happy birthday! You grew older.\n" +
                   "Your colleagues gave you a gift, it is here!" +
                   birthday_link),
                  EMAIL_ADDR,
                  [recipient_email])
        # ['tanyeejian@gmail.com']) # you can put your email here to test
