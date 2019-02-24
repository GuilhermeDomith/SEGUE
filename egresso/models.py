from django.db import models
from django.contrib.auth.models import User


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


class Egresso(models.Model):
    '''
        Os campos email e senha são herdados de User.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    matricula = models.CharField(max_length=30) #Unique, PK?
    #nome = models.CharField(max_length=30)  
    #sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=15) #Unique?
    identidade = models.CharField(max_length=15) #Unique?

    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=150)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=60)
    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return '%s, %s'%(self.user.username, self.matricula)

    def __repr__(self):
        return '%s, %s'%(self.user.username, self.matricula)


class Formacao_Escolar(models.Model):
    egresso = models.ForeignKey(
        Egresso,
        on_delete = models.CASCADE,
    )

    curso = models.ForeignKey(
        Curso, 
        on_delete=models.SET_NULL,
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
