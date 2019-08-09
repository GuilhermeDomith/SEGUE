from django.db import models
from empresa.models import Empresa
from egresso.models import Egresso
from curso.models import Curso, NivelCurso, AreaAtuacao
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
    tipo = models.ForeignKey(TipoOportunidade, on_delete=models.SET_NULL, null=True)
    horas_semana = models.IntegerField()
    cidade = models.CharField(max_length=60, blank=False, null=False)
    estado = models.CharField(max_length=2)
    nivel_necessario = models.ForeignKey(NivelCurso, on_delete=models.SET_NULL, null=True) 
    area_necessaria = models.ForeignKey(AreaAtuacao, on_delete=models.SET_NULL, null=True)

    def as_dict(self):
        dict = utils.to_dict(self)

        dict.update({
            'razao_social': self.empresa.razao_social,
            'email': self.empresa.user.email,
            'nivel_necessario': utils.to_dict(self.nivel_necessario),
            'area_necessaria': utils.to_dict(self.area_necessaria),
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