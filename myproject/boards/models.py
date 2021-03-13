from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HRPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Team(models.Model):
    name = models.CharField(max_length=100)
    hr_person = models.ForeignKey(to=HRPerson, on_delete=models.CASCADE)

class Person(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField(default='admin@admin.com')
    phone = models.IntegerField(default=12345678)
    is_support_person = models.BooleanField(default=False)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)

    def __eq__(self, other):
        if self.email is not None and other.email is not None:
            return self.email == other.email
        elif self.phone is not None and other.phone is not None:
            return self.phone == other.phone
        return False

class BirthdayEvent(models.Model):
    person = models.OneToOneField(to=Person, on_delete=models.PROTECT)
    date = models.DateField()
    event_link = models.CharField(max_length=1000)
