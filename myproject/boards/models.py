from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HRPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    hr_person = models.ForeignKey(to=HRPerson, on_delete=models.CASCADE)

class CorporateTeam(models.Model):
    name = models.CharField(max_length=100)
    hr_person = models.ForeignKey(to=HRPerson, on_delete=models.CASCADE)

class SupportTeam(models.Model):
    name = models.CharField(max_length=100)
    hr_person = models.ForeignKey(to=HRPerson, on_delete=models.CASCADE)

class CorporatePerson(Person):
    team = models.ForeignKey(to=CorporateTeam, on_delete=models.CASCADE)

class SupportPerson(Person):
    team = models.ForeignKey(to=SupportTeam, on_delete=models.CASCADE)

class BirthdayEvent(models.Model):
    person = models.OneToOneField(to=Person, on_delete=models.PROTECT)
    date = models.DateField()
    event_link = models.CharField(max_length=1000)
