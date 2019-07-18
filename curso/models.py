from django.db import models
from SEGUE import utils

class AreaAtuacao(models.Model):
    descricao = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Área Curso'
        verbose_name_plural = 'Áreas Curso'

    def as_dict(self):
        return utils.to_dict(self)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class NivelCurso(models.Model):
    descricao = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Nível Curso'
        verbose_name_plural = 'Níveis Curso'

    def as_dict(self):
        print('teste::', utils.to_dict(self))
        return utils.to_dict(self)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao



class Curso(models.Model):
    nome = models.CharField(max_length=100)

    nivel_curso = models.ForeignKey(NivelCurso, on_delete=models.SET_NULL, null=True) 
    area_atuacao = models.ForeignKey(AreaAtuacao, on_delete=models.SET_NULL, null=True)
    is_local = models.BooleanField('Curso Do Instituto', default=False) 

    def as_dict(self):
        dict = utils.to_dict(self)

        dict.update({
            'nivel_curso': self.nivel_curso.as_dict(),
            'area_atuacao': self.area_atuacao.as_dict(),
        })
        print(dict)

        return dict

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.nome
