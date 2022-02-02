# Generated by Django 3.0.5 on 2020-06-11 14:19

import Myapi.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0015_auto_20200611_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='certificate_name',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='institution',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='course',
            name='published',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='Myapi.Tag'),
        ),
        migrations.CreateModel(
            name='course_resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=300)),
                ('file', models.FileField(upload_to=Myapi.models.user_directory_path)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_material', to='Myapi.Course')),
            ],
        ),
    ]
