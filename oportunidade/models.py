from django.db import models
from empresa.models import Empresa
from egresso.models import Egresso
from curso.models import Curso, NivelCurso
from SEGUE import utils

class TipoOportunidade(models.Model):
    descricao = models.CharField(max_length=30)
    
    class Meta:
        verbose_name = 'Tipo de Oportunidade'
        verbose_name_plural = 'Tipos de oportunidade'

    def as_dict(self):
        return utils.to_dict(self)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Oportunidade(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE)
    titulo = models.CharField(max_length=100)
    horas_semana = models.IntegerField()
    tipo = models.ForeignKey(TipoOportunidade, on_delete=models.SET_NULL, null=True)
    curso_objetivo = models.OneToOneField(Curso, on_delete=models.SET_NULL, null=True)
    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=2)

    def as_dict(self):
        dict = utils.to_dict(self)

        dict.update({
            'curso_objetivo': utils.to_dict(self.curso_objetivo),
            'tipo': utils.to_dict(self.tipo),
        })
        
        return dict

    def __str__(self):
        return self.titulo

    def __repr__(self):
        return self.titulo


def obter_oportunidades(**args):
    try: return Oportunidade.objects.filter(**args)
    except: return []