# Generated by Django 4.0.2 on 2022-03-23 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_service_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.IntegerField(default=-1),
        ),
    ]
