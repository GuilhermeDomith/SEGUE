# Generated by Django 2.1.5 on 2019-03-06 19:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egresso', '0002_auto_20190306_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egresso',
            name='data_nascimento',
            field=models.DateField(default=datetime.datetime(2001, 3, 6, 19, 22, 21, 65574)),
        ),
    ]
