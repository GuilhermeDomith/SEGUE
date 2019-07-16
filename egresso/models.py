from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from curso.models import Curso, AreaAtuacao, NivelCurso
from SEGUE import settings, utils


class Escolaridade(models.Model):
    descricao = models.CharField(max_length=50)

    def as_dict(self):
        return utils.to_dict(self)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class Genero(models.Model):
    descricao = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

    def as_dict(self):
        return utils.to_dict(self)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return self.descricao


class EstadoCivil(models.Model):
    descricao = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Estado Civil'
        verbose_name_plural = 'Estados Civís'

    def as_dict(self):
        return utils.to_dict(self)

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

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def as_dict(self):
        return utils.to_dict(self)

    def __str__(self):
        return '%s, %s, %s'%(self.cidade, self.rua, self.cep)

    def __repr__(self):
        return str(self)

    
class DadosPessoais(models.Model):
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, blank=True, null=True)
    identidade = models.CharField(max_length=15, blank=True, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.SET_NULL, null=True)
    data_nascimento = models.DateField(default=datetime.now() - relativedelta(years=18))
    celular = models.CharField(max_length=20, blank=True, null=True)
    carteira_motorista = models.CharField(max_length=5, blank=True, null=True)
    escolaridade_mae = models.CharField(max_length=80, blank=True, null=True)
    escolaridade_pai = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        verbose_name = 'Dados Pessoais'
        verbose_name_plural = verbose_name

    def as_dict(self):
        dict = utils.to_dict(self)

        dict.update({
            'idade': self.get_idade(),
            'estado_civil': self.estado_civil.descricao if self.estado_civil else None,
            'genero': self.genero.descricao if self.genero else None,
        })

        return dict

    def get_idade(self):
        now = datetime.today()
        dn = self.data_nascimento    
        if not dn:
            return 0
        return now.year - dn.year - ((now.month, now.day) < (dn.month, dn.day))

    def __str__(self):
        return '%s, %s'%(self.cpf, self.nome_completo)

    def __repr__(self):
        return str(self)


class PerfilSites(models.Model):
    link_linkedin = models.CharField(max_length=250, blank=True, null=True)
    link_lattes = models.CharField(max_length=250, blank=True, null=True)
    link_github = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil Sites'
        verbose_name_plural = verbose_name

    def as_dict(self):
        return utils.to_dict(self)


class Egresso(models.Model):
    ''' Os campos email e senha são herdados de User.'''

    matricula = models.CharField(max_length=30) #será unique
    is_aluno = models.BooleanField('aluno status', default=False, help_text=_('Designado quando o usuário cadastrado ainda é aluno.'))

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    dados = models.OneToOneField(DadosPessoais, on_delete=models.SET_NULL, null=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.SET_NULL, null=True)
    perfil_sites = models.OneToOneField(PerfilSites, on_delete=models.SET_NULL, null=True)
    raio_atuacao_max = models.IntegerField(default=0, help_text='Raio de distância (Km) para encontrar oportunidades.')

    def get_endereco(self):
        try: return self.endereco
        except Egresso.DoesNotExist: return None

    def get_formacoes(self):
        try: return self.formacao_set.all()
        except Egresso.DoesNotExist: return None
    
    def get_formacoes_dict(self):
        formacoes = self.get_formacoes()
        return [f.as_dict() for f in formacoes]

    def as_dict(self):
        dict = utils.to_dict(self)

        dict.update({
            'email': self.user.email,
            'dados': self.dados.as_dict() if self.dados else {},
            'endereco': self.endereco.as_dict() if self.endereco else {},
            'perfil_sites': self.perfil_sites.as_dict() if self.perfil_sites else {}
        })

        print(dict)

        return dict

    def __str__(self):
        return '%s, %s'%(self.user.email, self.matricula)

    def __repr__(self):
        return '%s, %s'%(self.user.email, self.matricula)


class Formacao(models.Model):
    egresso = models.ForeignKey(Egresso, on_delete = models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ano_inicio = models.IntegerField()
    ano_termino = models.IntegerField()

    class Meta:
        verbose_name = 'Formação Acadêmica'
        verbose_name_plural = 'Formações Acadêmicas'

    def as_dict(self):
        dict = utils.to_dict(self)


        dict.update({
            'curso': self.curso.as_dict() if self.curso else {},
        })

        return dict

    def __str__(self):
        return '%s, %s'#%(self.egresso.user.email, self.curso)

    def __repr__(self):
        return str(self)


def obter_formacoes(**args):
    try:
        return Formacao.objects.filter(**args)
    except:
        return []


def obter_egresso(**args):
    try: 
        egresso = Egresso.objects.get(**args)
        return egresso
    except Egresso.DoesNotExist:
        return None

    