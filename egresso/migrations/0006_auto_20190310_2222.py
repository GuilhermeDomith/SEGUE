# Generated by Django 2.1.5 on 2019-03-10 22:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egresso', '0005_auto_20190310_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egresso',
            name='data_nascimento',
            field=models.DateField(default=datetime.datetime(2001, 3, 10, 22, 22, 34, 361211)),
        ),
    ]