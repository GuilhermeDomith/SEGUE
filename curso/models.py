from django.db import models

class Area_Curso(models.Model):
    descricao = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Área Curso'
        verbose_name_plural = 'Áreas Curso'

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Curso(models.Model):
    nome = models.CharField(max_length=80)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.nome


class Nivel_Curso(models.Model):
    descricao = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Nível Curso'
        verbose_name_plural = 'Níveis Curso'

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao