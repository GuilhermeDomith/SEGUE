# Generated by Django 2.2.1 on 2019-08-09 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionario', '0004_auto_20190808_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questao',
            name='habilitar_opcao_outro',
            field=models.BooleanField(default=False, help_text='Permite que o egresso forneça uma outra resposta', verbose_name='Permitir outra resposta'),
        ),
        migrations.AlterField(
            model_name='questionario',
            name='anos_corridos',
            field=models.IntegerField(unique=True, verbose_name='Responder depois de quantos após formar'),
        ),
        migrations.AlterField(
            model_name='respostaquestionario',
            name='questao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questionario.Questao'),
        ),
        migrations.AlterField(
            model_name='respostaquestionario',
            name='questionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='questionario.Questionario'),
        ),
    ]
