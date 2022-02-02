# Generated by Django 3.0.5 on 2020-06-11 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapi', '0012_auto_20200611_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=35)),
                ('slug', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='tags',
        ),
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='Myapi.Tag'),
        ),
    ]