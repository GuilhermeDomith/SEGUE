from django.db import models

from egresso.models import NivelCurso, Curso, Formacao
from curso.models import Curso, AreaAtuacao, NivelCurso
from SEGUE import settings, utils


class Empresa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=20)

    def get_oportunidades(self):
        try:
            return self.oportunidade_set.all()
        except:
            return []

    def as_dict(self):
        data = utils.to_dict(self)
        print('\n\n', self.user_id, '\n\n')
        data.update(user_id=self.user_id)
        return data

    def __str__(self):
        return self.razao_social or self.user.email

    def __repr__(self):
        return str(self)


def obter_empresa(**args):
    try:
        empresa = Empresa.objects.get(**args)
        return empresa
    except Empresa.DoesNotExist:
        return None