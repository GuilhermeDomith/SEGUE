from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Area_Curso(models.Model):
    descricao = models.CharField(max_length=100)

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


class Nivel_Formacao(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Endereco(models.Model):
    cep = models.CharField(max_length=15, blank=True, null=True)
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=60)
    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return '%s, %s, %s'%(self.cidade, self.rua, self.cep)

    def __repr__(self):
        return '%s, %s, %s'%(self.cidade, self.rua, self.cep)

    def form_to_dict(form_dict):
        return {'cep': form_dict['cep'],
            'rua': form_dict['rua'],
            'numero': form_dict['numero'],
            'complemento': form_dict['complemento'],
            'bairro': form_dict['bairro'],
            'cidade': form_dict['cidade'],
            'estado': form_dict['estado'],
        }


class Egresso(models.Model):
    '''
        Os campos email e senha são herdados de User.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=30, unique=True)
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField(default=datetime.now() - relativedelta(years=18))
    cpf = models.CharField(max_length=15, blank=True, null=True)
    identidade = models.CharField(max_length=15, blank=True, null=True)

    link_likedin = models.CharField(max_length=250, blank=True, null=True)
    link_lattes = models.CharField(max_length=250, blank=True, null=True)
    link_github = models.CharField(max_length=250, blank=True, null=True)

    endereco = models.OneToOneField(
        Endereco,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return '%s, %s'%(self.user.username, self.matricula)

    def __repr__(self):
        return '%s, %s'%(self.user.username, self.matricula)

    def form_to_dict(form_dict):
        return {'matricula': form_dict['matricula'],
            'nome_completo': form_dict['nome_completo'],
            'data_nascimento': form_dict['data_nascimento'],
            'cpf': form_dict['cpf'],
            'identidade': form_dict['identidade'],
            }


class Formacao_Escolar(models.Model):
    egresso = models.ForeignKey(
        Egresso,
        on_delete = models.CASCADE,
    )

    curso = models.ForeignKey(
        Curso, 
        on_delete=models.SET_NULL, # Poderia ser null=False e on_delete=CASCADE
        null=True
    )

    area = models.ForeignKey(
        Area_Curso, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True 
    )

    ano_inicio = models.IntegerField(default=0)
    ano_termino = models.IntegerField(default=0)

    nivel_formacao = models.ForeignKey(
        Nivel_Formacao,
        on_delete=models.SET_NULL,
        null=True
    ) 

    def __str__(self):
        return '%s, %s'%(self.egresso.user.username, self.curso)

    def __repr__(self):
        return '%s, %s'%(self.egresso.user.username, self.curso)
