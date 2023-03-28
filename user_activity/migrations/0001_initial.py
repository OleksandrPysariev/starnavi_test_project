# Generated by Django 4.1.7 on 2023-03-27 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(default=datetime.datetime.now)),
                ('last_activity', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]