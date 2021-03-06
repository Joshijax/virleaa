# Generated by Django 3.0.5 on 2020-05-14 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(max_length=100)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapi.Course')),
            ],
        ),
        migrations.CreateModel(
            name='section_material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=200)),
                ('file', models.CharField(max_length=200)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapi.Course_content')),
            ],
        ),
    ]
