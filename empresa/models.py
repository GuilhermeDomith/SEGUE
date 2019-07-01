from django.db import models

from egresso.models import NivelCurso, Curso, Formacao
from curso.models import Curso, AreaAtuacao, NivelCurso
from SEGUE import settings, utils


class Empresa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=20)


    def get_oportunidades(self):
        try:
            return self.oportunidade_set.all()
        except:
            return []

    def as_dict(self):
        return utils.to_dict(self)

    def __str__(self):
        return self.razao_social

    def __repr__(self):
        return self.razao_social


def obter_empresa_user(user):
    try:
        empresa = Empresa.objects.get(user=user)
        return empresa
    except Empresa.DoesNotExist:
        return None