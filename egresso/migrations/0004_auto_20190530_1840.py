# Generated by Django 2.2.1 on 2019-05-30 18:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egresso', '0003_auto_20190404_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egresso',
            name='data_nascimento',
            field=models.DateField(default=datetime.datetime(2001, 5, 30, 18, 40, 4, 86586)),
        ),
    ]