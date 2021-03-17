from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, send_mass_mail
from boards.models import BirthdayEvent, Person
from myproject.settings import EMAIL_HOST_USER as HOST_EMAIL_ADDR
from myproject.settings import NEXMO_CLIENT_KEY, NEXMO_CLIENT_SECRET, SMS_CLIENT_HOST
import datetime
import nexmo

INVITE_DAYS_BEFORE = 14
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
        birthday_events = BirthdayEvent.objects.filter(
            date__day=birthday_date.day
        ).filter(date__month=birthday_date.month)
        for event in birthday_events:
            friends = self.get_friends(event.person)
            assert event.person not in friends
            self.invite_all(event.person, event.event_link, friends)

    def handle_reminders(self):
        """
        We fetch birthday events that will happen in REMINDER_DAYS_BEFORE
        and send emails.
        """
        birthday_date = datetime.date.today() + datetime.timedelta(
            days=REMINDER_DAYS_BEFORE
        )
        birthday_events = BirthdayEvent.objects.filter(
            date__day=birthday_date.day
        ).filter(date__month=birthday_date.month)
        for event in birthday_events:
            friends = self.get_friends(event.person)
            assert event.person not in friends
            self.remind_all(event.person, event.event_link, friends)

    def handle_on_birthday(self):
        today = datetime.date.today()
        birthday_events = BirthdayEvent.objects.filter(date__day=today.day).filter(
            date__month=today.month
        )
        for event in birthday_events:
            age = today.year - event.person.birthday.year
            self.celebrate(event.person, event, age)

    ####################
    # HELPER FUNCTIONS #
    ####################
    def send_sms(self, invitation, friend):
        print(f"sending sms to {friend.phone}")
        self.sms_client.send_message(
            {
                "from": SMS_CLIENT_HOST,
                "to": f"{COUNTRY_CODE}{friend.phone}",
                "text": invitation["content"],
            }
        )

    def send_email(self, invitation, friend):
        print(f"sending email to {friend.email}")
        send_mail(
            invitation["title"], invitation["content"], HOST_EMAIL_ADDR, [friend.email]
        )

    def invite_all(self, birthday_person, birthday_link, friends):
        for friend in friends:
            invitation = self.create_invitation(birthday_person, birthday_link, friend)
            if friend.is_support_person:
                self.send_sms(invitation, friend)
            else:
                self.send_email(invitation, friend)

    def remind_all(self, birthday_person, birthday_link, friends):
        for friend in friends:
            reminder = self.create_reminder(birthday_person, birthday_link, friend)
            if friend.is_support_person:
                self.send_sms(reminder, friend)
            else:
                self.send_email(reminder, friend)

    def celebrate(self, person, event, age):
        celebration = self.create_celebration(person, event.event_link, age)
        if person.is_support_person:
            self.send_sms(celebration, person)
        else:
            self.send_email(celebration, person)

    def create_invitation(self, birthday_person, birthday_link, person):
        return {
            "title": f"Invitation for {birthday_person}'s birthday",
            "content": (
                f"Hey {person.name},\n"
                + f"It's {birthday_person.name}'s birthday in {INVITE_DAYS_BEFORE} days time!"
                + f"{birthday_person.name} is from the {birthday_person.team} team and this is the link to the Gift-It-Forward page: {birthday_link}.\n"
                + f"Warm regards,"
                + f"Company HR"
            ),
        }

    def create_reminder(self, birthday_person, birthday_link, person):
        return {
            "title": f"Reminder for {birthday_person}'s birthday",
            "content": (
                f"Hey {person.name},\n"
                + f"It's {birthday_person.name}'s birthday in {REMINDER_DAYS_BEFORE} days time!"
                + f"{birthday_person.name} is from the {birthday_person.team} team and this is the link to the Gift-It-Forward page: {birthday_link}.\n"
                + f"Warm regards,"
                + f"Company HR"
            ),
        }

    def create_celebration(self, birthday_person, event_link, age):
        return {
            "title": f"Happy Birthday {birthday_person}!",
            "content": (
                f"Hey {birthday_person.name},\n"
                + f"Thank you for your contributions to the company and we would like to wish you a Happy {ordinal(age)} birthday!"
                + "Please click on this link to claim your birthday gift!"
                + event_link
            ),
        }

    def get_friends(self, person):
        friends = Person.objects.exclude(name__exact=person.name)
        # if not a support staff then just inform the person's team
        if not person.is_support_person:
            friends = friends.filter(team__exact=person.team)
        return friends
