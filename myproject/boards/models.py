from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from datetime import datetime

# Create your models here.
class HRPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Team(models.Model):
    name = models.CharField(max_length=100)
    hr_person = models.ForeignKey(to=HRPerson, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField(default='admin@admin.com')
    phone = models.IntegerField(default=12345678)
    is_support_person = models.BooleanField(default=False)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)

class BirthdayEvent(models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    event_link = models.CharField(max_length=1000)
