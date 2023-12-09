# Generated by Django 4.1.7 on 2023-12-09 10:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_alter_attendees_created_alter_prayerrequest_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialcard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('pastor', models.BooleanField(default=False)),
                ('level', models.CharField(choices=[('1', 'Level 1'), ('2', 'Level 2'), ('3', 'Level 3')], max_length=8)),
                ('created', models.DateTimeField(default=datetime.datetime(2023, 12, 9, 10, 47, 39, 342751, tzinfo=datetime.timezone.utc))),
            ],
        ),
        migrations.AlterField(
            model_name='attendees',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='prayerrequest',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 10, 47, 39, 342751, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='volunteers',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 10, 47, 39, 342751, tzinfo=datetime.timezone.utc)),
        ),
    ]