# Generated by Django 3.1.7 on 2021-03-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_person_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_support_person',
            field=models.BooleanField(default=False),
        ),
    ]
