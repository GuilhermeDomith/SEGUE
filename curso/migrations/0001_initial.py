# Generated by Django 2.2.1 on 2019-07-18 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AreaAtuacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Área Curso',
                'verbose_name_plural': 'Áreas Curso',
            },
        ),
        migrations.CreateModel(
            name='NivelCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Nível Curso',
                'verbose_name_plural': 'Níveis Curso',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('is_local', models.BooleanField(default=False, verbose_name='Curso Do Instituto')),
                ('area_atuacao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='curso.AreaAtuacao')),
                ('nivel_curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='curso.NivelCurso')),
            ],
        ),
    ]
