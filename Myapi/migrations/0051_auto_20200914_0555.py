# Generated by Django 2.2.10 on 2020-09-14 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0050_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rating', to='Myapi.Course'),
        ),
    ]