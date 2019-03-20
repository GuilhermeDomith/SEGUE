from django.db import models
from empresa.models import Empresa
from egresso.models import Egresso
from curso.models import Curso, Nivel_Curso

class Tipo_Oportunidade(models.Model):
    descricao = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = 'Tipo de Oportunidade'
        verbose_name_plural = 'Tipos de oportunidade'

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Oportunidade(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete = models.CASCADE,
    )

    titulo = models.CharField(max_length=50)
    horas_semana = models.IntegerField()

    curso_necessario = models.ForeignKey(
        Curso,
        on_delete=models.SET_NULL,
        null=True
    )

    nivel_formacao = models.ForeignKey(
        Nivel_Curso,
        on_delete=models.SET_NULL,
        null=True
    )

    tipo = models.ForeignKey(
        Tipo_Oportunidade,
        on_delete=models.SET_NULL,
        null=True
    )

    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=2)

    def get_oportunidades(**args):
        try: return Oportunidade.objects.filter(**args)
        except: return []

    '''def get_dict_detalhado(self):
        dict = self.as_dict()

        try:
            formacoes = Formacao_Academica.objects.filter(
                curso_id=self.curso_necessario_id, 
                nivel_formacao=self.nivel_formacao
            )

            egressos = [ f.egresso.dict() for f in formacoes]
        except Exception as e:
            egressos = []
    

        dict.update({
            'egressos': egressos
        })

        return dict'''

    def as_dict(self):
        dict = self.__dict__

        dict.update({
            'curso_necessario': self.curso_necessario.nome,
            'nivel_formacao': self.nivel_formacao.descricao,
            'tipo': self.tipo.descricao,
        })
        return dict

    def __str__(self):
        return self.titulo

    def __repr__(self):
        return self.titulo