# Generated by Django 2.2.10 on 2020-07-13 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0033_auto_20200703_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='publish',
            field=models.BooleanField(default='False'),
        ),
    ]
