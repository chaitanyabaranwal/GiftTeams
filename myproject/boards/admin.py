from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(HRPerson)
admin.site.register(Person)
admin.site.register(Team)
admin.site.register(BirthdayEvent)