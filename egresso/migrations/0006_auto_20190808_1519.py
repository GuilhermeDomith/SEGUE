# Generated by Django 2.2.1 on 2019-08-08 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egresso', '0005_auto_20190808_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadospessoais',
            name='data_nascimento',
            field=models.DateField(default=datetime.datetime(2001, 8, 8, 15, 19, 19, 961379)),
        ),
    ]