# Generated by Django 2.2.1 on 2019-07-15 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curso', '0002_auto_20190621_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='is_local',
            field=models.BooleanField(default=False, verbose_name='Curso Do Instituto'),
        ),
    ]
