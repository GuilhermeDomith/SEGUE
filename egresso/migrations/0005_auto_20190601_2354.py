# Generated by Django 2.2.1 on 2019-06-01 23:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egresso', '0004_auto_20190530_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egresso',
            name='data_nascimento',
            field=models.DateField(default=datetime.datetime(2001, 6, 1, 23, 54, 6, 430749)),
        ),
    ]
