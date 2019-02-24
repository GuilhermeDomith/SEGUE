# Generated by Django 2.1.5 on 2019-02-24 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area_Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Egresso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=30)),
                ('data_nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=15)),
                ('identidade', models.CharField(max_length=15)),
                ('cep', models.CharField(max_length=15)),
                ('rua', models.CharField(max_length=150)),
                ('numero', models.IntegerField()),
                ('bairro', models.CharField(max_length=60)),
                ('cidade', models.CharField(max_length=60)),
                ('estado', models.CharField(max_length=2)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Formacao_Escolar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_inicio', models.IntegerField(default=0)),
                ('ano_termino', models.IntegerField(default=0)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='egresso.Area_Curso')),
                ('curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='egresso.Curso')),
                ('egresso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='egresso.Egresso')),
            ],
        ),
        migrations.CreateModel(
            name='Nivel_Formacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='formacao_escolar',
            name='nivel_formacao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='egresso.Nivel_Formacao'),
        ),
    ]