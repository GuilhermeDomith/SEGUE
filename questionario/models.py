from django.db import models
from SEGUE import settings, utils
from egresso.models import Formacao

class PossivelResposta(models.Model):
    resposta = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Possível Resposta'
        verbose_name_plural = 'Possíveis Respostas'

    def as_dict(self):
        dict = utils.to_dict(self)
        return dict

    def __str__(self):
        return 'OP%s - %s'%(self.id, self.resposta)

    def __repr__(self):
        return str(self)


class Questao(models.Model):
    pergunta = models.CharField(max_length=255)
    possiveis_respostas = models.ManyToManyField(PossivelResposta)
    habilitar_opcao_outro = models.BooleanField('Permitir outra resposta', default=False, help_text='Permite que o egresso forneça uma outra resposta')

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

    def as_dict(self):
        dict = utils.to_dict(self)

        dict.update({
            'possiveis_respostas': [r.as_dict() for r in self.possiveis_respostas.all()],
        })
        return dict

    def __str__(self):
        return 'Q%s - %s'%(self.id, self.pergunta)

    def __repr__(self):
        return str(self)
    

class Questionario(models.Model):
    anos_corridos = models.IntegerField('Responder depois de quantos após formar', unique=True)
    questoes = models.ManyToManyField(Questao)

    class Meta:
        verbose_name = 'Questionário'
        verbose_name_plural = 'Questionários'

    def as_dict(self):
        dict = utils.to_dict(self)

        dict.update({
            'questoes': [q.as_dict() for q in self.questoes.all()],
        })
        return dict

    def __str__(self):
        return 'Questionario %s ano(s);'%(self.anos_corridos)

    def __repr__(self):
        return str(self)


class RespostaQuestionario(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.PROTECT)
    resposta = models.CharField(max_length=255)
    questionario = models.ForeignKey(Questionario, on_delete=models.PROTECT)
    formacao = models.ForeignKey(Formacao, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Resposta Questionário'
        verbose_name_plural = 'Respostas Questionário'

    def as_dict(self):
        dict = utils.to_dict(self)
        return dict

    def __str__(self):
        return '%s - Q%sQ%s - R: %s'%(
            self.formacao.egresso.user.email,
            self.questionario.id, 
            self.questao.id,
            self.resposta
            )

    def __repr__(self):
        return str(self)


