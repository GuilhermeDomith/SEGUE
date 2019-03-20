from django.db import models

from egresso.models import Nivel_Curso, Curso, Formacao_Academica
from curso.models import Curso, Area_Curso, Nivel_Curso
from SEGUE import settings


class Area_Atuacao_Empresa(models.Model):
    descricao = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Área de Atuação'
        verbose_name_plural = 'Áreas de Atuação'

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Empresa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=20)

    area_atuacao = models.ForeignKey(
        Area_Atuacao_Empresa,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def get_oportunidades(self):
        try:
            return self.oportunidade_set.all()
        except:
            return []

    def get_empresa_user(user):
        try:
            empresa = Empresa.objects.get(user=user)
            return empresa
        except Empresa.DoesNotExist:
            return None

    def __str__(self):
        return self.razao_social

    def __repr__(self):
        return self.razao_social

