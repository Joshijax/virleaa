# Generated by Django 2.2.10 on 2020-07-13 11:23

import Myapi.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0036_auto_20200713_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='file',
            field=models.FileField(blank=True, upload_to=Myapi.models.user_directory_path1),
        ),
    ]