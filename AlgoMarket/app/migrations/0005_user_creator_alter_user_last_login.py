# Generated by Django 4.0.2 on 2022-03-17 23:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_activate_service_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='creator',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.TimeField(default=datetime.datetime(2022, 3, 17, 16, 46, 59, 670388)),
        ),
    ]
