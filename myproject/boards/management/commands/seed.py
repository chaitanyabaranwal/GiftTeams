from django.core.management.base import BaseCommand, CommandError
from boards.models import *
from faker import Faker

import random

fake = Faker()

class Command(BaseCommand):

    def make_user(self):
        return User.objects.create(
            username = fake.user_name(),
            email = fake.email(),
            password = fake.password(),
            first_name = fake.first_name(),
            last_name = fake.last_name(),
        )

    def make_hrperson(self):
        return self._make_hrperson(self.make_user())

    def _make_hrperson(self, user):
        hrperson = HRPerson.objects.create(user=user)
        # print(hrperson)
        return hrperson

    def make_teams(self):
        hrperson = self.make_hrperson()
        return [self._make_team(hrperson) for _ in range(random.randint(1,10))]

    def _make_team(self, hrperson):
        team =  Team.objects.create(
            name=fake.catch_phrase(),
            hr_person=hrperson
        )
        # print(team)
        return team

    def make_people(self, team):
        # 20% probability of a team being support team
        is_support_team = fake.boolean(20)
        return [self.make_person(team, is_support_team) for _ in range(random.randint(5,25))]

    def make_person(self, team, is_support_team):
        person =  Person.objects.create(
            name=fake.name(),
            birthday=fake.date(),
            email=fake.email(),
            phone=random.randint(80000000, 90000000),
            is_support_person=is_support_team,
            team=team
        )
        # print(person)
        return person

    def make_birthday(self, person):
        bd = BirthdayEvent.objects.create(
            person=person,
            event_link=fake.url()+fake.password(special_chars=False)
        )
        # print(bd)
        return bd

    def handle(self, *args, **options):
        teams = self.make_teams()
        print(f"Made {len(teams)} teams.")
        for team in teams:
            people = self.make_people(team)
            print(f"Team {team} has {len(people)} members.")
            for person in people:
                bd = self.make_birthday(person)
                print(f"{person} has birthday on {person.birthday}.")