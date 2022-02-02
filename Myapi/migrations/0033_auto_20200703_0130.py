# Generated by Django 2.2.10 on 2020-07-03 00:30

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0032_remove_course_fr_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]