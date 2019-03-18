# Generated by Django 2.1.5 on 2019-03-17 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('egresso', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area_Atuacao_Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razao_social', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=18)),
                ('telefone', models.CharField(max_length=20)),
                ('area_atuacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresa.Area_Atuacao_Empresa')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Oportunidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('horas_semana', models.IntegerField()),
                ('cidade', models.CharField(max_length=60)),
                ('estado', models.CharField(max_length=2)),
                ('curso_necessario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='egresso.Curso')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresa.Empresa')),
                ('nivel_formacao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='egresso.Nivel_Formacao')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Oportunidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='oportunidade',
            name='tipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresa.Tipo_Oportunidade'),
        ),
    ]
