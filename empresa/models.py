from django.db import models
from egresso.models import Nivel_Formacao, Curso, Formacao_Academica
from SEGUE import settings


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


class Tipo_Oportunidade(models.Model):
    descricao = models.CharField(max_length=30)

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
        Nivel_Formacao,
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

    def get_dict_detalhado(self):
        dict = self.as_dict()

        try:
            formacoes = Formacao_Academica.objects.filter(
                curso_id=self.curso_necessario_id, 
                nivel_formacao=self.nivel_formacao
            )

            egressos = [ f.egresso.dict() for f in formacoes]
        except Exception as e:
            print(e)
            egressos = []
    

        dict.update({
            'egressos': egressos
        })

        return dict

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
