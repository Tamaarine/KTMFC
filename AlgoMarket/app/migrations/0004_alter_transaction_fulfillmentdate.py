# Generated by Django 4.0.2 on 2022-03-30 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_transaction_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='fulfillmentDate',
            field=models.TimeField(null=True),
        ),
    ]
