# Generated by Django 3.0.5 on 2020-05-14 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0002_course_content_section_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_content',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_content', to='Myapi.Course'),
        ),
    ]