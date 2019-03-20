from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import datetime

from curso.models import Curso, Area_Curso, Nivel_Curso
from SEGUE import settings



class Endereco(models.Model):
    cep = models.CharField(max_length=15, blank=True, null=True)
    rua = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=60)
    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=2)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return '%s, %s, %s'%(self.cidade, self.rua, self.cep)

    def __repr__(self):
        return '%s, %s, %s'%(self.cidade, self.rua, self.cep)

    


class Egresso(models.Model):
    '''
        Os campos email e senha são herdados de User.
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=30, unique=True)
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField(default=datetime.now() - relativedelta(years=18))
    cpf = models.CharField(max_length=15, blank=True, null=True)
    identidade = models.CharField(max_length=15, blank=True, null=True)

    link_linkedin = models.CharField(max_length=250, blank=True, null=True)
    link_lattes = models.CharField(max_length=250, blank=True, null=True)
    link_github = models.CharField(max_length=250, blank=True, null=True)

    endereco = models.OneToOneField(
        Endereco,
        on_delete=models.SET_NULL,
        null=True
    )

    def get_endereco(self):
        try:
            return self.endereco
        except Egresso.DoesNotExist:
            return None

    def get_egresso_user(user):
        try: 
            egresso = Egresso.objects.get(user=user)
            return egresso
        except Egresso.DoesNotExist:
            return None

    def get_idade(self):
        now = datetime.today()
        dn = self.data_nascimento
        if not dn:
            return 0

        return now.year - dn.year - ((now.month, now.day) < (dn.month, dn.day))

    def get_formacoes(self):
        try:
            return self.formacao_academica_set.all()
        except Egresso.DoesNotExist:
            return None

    def as_dict(self):
        dict = super(Egresso, self).__dict__
        dict['email'] = self.user.email
        dict.update({'idade': self.get_idade()})

        try: 
            endereco = self.endereco.__dict__
            del endereco['id']
        except:
            endereco = {}

        dict.update(endereco)
        return dict

    def __str__(self):
        return '%s, %s'%(self.user.email, self.matricula)

    def __repr__(self):
        return '%s, %s'%(self.user.email, self.matricula)



class Formacao_Academica(models.Model):
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
        Nivel_Curso,
        on_delete=models.SET_NULL,
        null=True
    ) 

    class Meta:
        verbose_name = 'Formação Acadêmica'
        verbose_name_plural = 'Formações Acadêmicas'

    def get_formacoes(**args):
        try:
            return Formacao_Academica.objects.filter(**args)
        except:
            return []

    def as_dict(self):
        dict = self.__dict__

        try: area = self.area.descricao
        except Exception as e: area = ''

        dict.update({
            'curso': self.curso.nome,
            'area': area,
            'nivel_formacao': self.nivel_formacao.descricao,
        })

        return dict


    def __str__(self):
        return '%s, %s'%(self.egresso.user.email, self.curso)

    def __repr__(self):
        return '%s, %s'%(self.egresso.user.email, self.curso)
