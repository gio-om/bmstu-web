# Generated by Django 4.2.7 on 2024-10-02 08:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orion', '0004_alter_astronautflight_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 2, 8, 55, 53, 278633, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
    ]
