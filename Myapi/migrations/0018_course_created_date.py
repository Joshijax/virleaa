# Generated by Django 3.0.5 on 2020-06-11 18:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0017_auto_20200611_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
