# Generated by Django 3.0.5 on 2020-05-24 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0009_course_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='Course_Language',
        ),
    ]