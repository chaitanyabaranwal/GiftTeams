# Generated by Django 3.1.7 on 2021-03-16 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0010_auto_20210316_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthdayevent',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.person'),
        ),
    ]