from django.db import models
from django.contrib.auth.models import User
from egresso.models import Nivel_Formacao, Curso


class Area_Atuacao_Empresa(models.Model):
    descricao = models.CharField(max_length=150)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Empresa(models.Model):
    '''
        Os campos email e senha são herdados de User.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=20)

    area_atuacao = models.ForeignKey(
        Area_Atuacao_Empresa,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.razao_social

    def __repr__(self):
        return self.razao_social


class Tipo_Oportunidade(models.Model):
    descricao = models.CharField(max_length=30)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Oportunidade(models.Model):
    titulo = models.CharField(max_length=50)
    horas_semana = models.IntegerField()

    curso_necessario = models.ForeignKey(
        Curso, 
        on_delete=models.SET_NULL,
        null=True
    )

    nivel_formacao = models.ForeignKey(
        Nivel_Formacao,
        on_delete=models.SET_NULL,
        null=True
    ) 

    tipo = models.ForeignKey(
        Tipo_Oportunidade, 
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.titulo

    def __repr__(self):
        return self.titulo


