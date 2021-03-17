from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, send_mass_mail
from boards.models import BirthdayEvent, Person
from myproject.settings import EMAIL_HOST_USER as HOST_EMAIL_ADDR
from myproject.settings import NEXMO_CLIENT_KEY, NEXMO_CLIENT_SECRET, SMS_CLIENT_HOST
import datetime
import nexmo

INVITE_DAYS_BEFORE = 7
REMINDER_DAYS_BEFORE = 7
COUNTRY_CODE = "65"

# helper function to turn 1 into 1st etc
ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # Entry point
    def handle(self, *args, **options):
        """
        We send out scheduled emails on three cases:
        1. One week before birthday to friends.
        2. One day before birthday to friends.
        3. On the birthday to the person.
        """
        # register SMS client
        self.sms_client = nexmo.Client(key=NEXMO_CLIENT_KEY, secret=NEXMO_CLIENT_SECRET)

        self.handle_invites()
        self.handle_reminders()
        self.handle_on_birthday()

    def handle_invites(self):
        """
        We fetch birthday events that will happen in INVITE_DAYS_BEFORE
        days and send emails.
        """
        birthday_date = datetime.date.today() + datetime.timedelta(
            days=INVITE_DAYS_BEFORE
        )
        birthday_people = Person.objects.filter(birthday__day=birthday_date.day).filter(
            birthday__month=birthday_date.month
        )
        for person in birthday_people:
            friends = get_friends(person)
            event = BirthdayEvent.objects.get(person=person)
            assert person not in friends
            self.invite_all(person, event.event_link, friends)

    def handle_reminders(self):
        """
        We fetch birthday events that will happen in REMINDER_DAYS_BEFORE
        and send emails.
        """
        birthday_date = datetime.date.today() + datetime.timedelta(
            days=REMINDER_DAYS_BEFORE
        )
        birthday_people = Person.objects.filter(birthday__day=birthday_date.day).filter(
            birthday__month=birthday_date.month
        )
        for person in birthday_people:
            friends = get_friends(person)
            event = BirthdayEvent.objects.get(person=person)
            assert person not in friends
            self.remind_all(person, event.event_link, friends)

    def handle_on_birthday(self):
        today = datetime.date.today() + datetime.timedelta(days=REMINDER_DAYS_BEFORE)
        birthday_people = Person.objects.filter(birthday__day=today.day).filter(
            birthday__month=today.month
        )
        for person in birthday_people:
            event = BirthdayEvent.objects.get(person=person)
            age = today.year - person.birthday.year
            self.celebrate(person, event, age)

    ####################
    # HELPER FUNCTIONS #
    ####################
    def send_sms(self, invitation, friend):
        self.sms_client.send_message(
            {
                "from": SMS_CLIENT_HOST,
                "to": f"{COUNTRY_CODE}{friend.phone}",
                "text": invitation["content"],
            }
        )

    def send_email(self, invitation, friend):
        send_mail(
            invitation["title"], invitation["content"], HOST_EMAIL_ADDR, [friend.email]
        )

    def invite_all(self, birthday_person, birthday_link, friends):
        invitation = self.create_invitation(birthday_person, birthday_link)
        for friend in friends:
            if friend.is_support_staff:
                self.send_sms(invitation, friend)
            else:
                self.send_email(invitation, friend)

    def remind_all(self, birthday_person, birthday_link, friends):
        reminder = self.create_reminder(birthday_person, birthday_link)
        for friend in friends:
            if friend.is_support_staff:
                self.send_sms(reminder, friend)
            else:
                self.send_email(reminder, friend)

    def celebrate(self, person, event, age):
        celebration = self.create_celebration(person, event.event_link, age)
        if person.is_support_staff:
            self.send_sms(celebration, person)
        else:
            self.send_email(celebration, person)

    def create_invitation(self, birthday_person, birthday_link):
        return {
            "title": f"{birthday_person}'s birthday",
            "content": f"{birthday_person} birthday liao give money pls thx {birthday_link}",
        }

    def create_reminder(self, birthday_person, birthday_link):
        return {
            "title": f"Last Reminder: {birthday_person}'s birthday",
            "content": f"{birthday_person} birthday tmr give money pls thx {birthday_link}",
        }

    def create_celebration(self, birthday_person, event_link, age):
        return {
            "title": f"Happy Birthday {birthday_person}!",
            "content": (
                "Happy {ordinal(age)} birthday!"
                + "Check out the collective gift by your colleagues here!"
                + event_link
            ),
        }

    def get_friends(self, person):
        friends = Person.objects.exclude(name__exact=person.name)
        # if not a support staff then just inform the person's team
        if not person.is_support_person:
            friends = friends.filter(team__exact=person.team)
        return friends
