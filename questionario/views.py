from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from SEGUE.decorators import is_user

#from .models import TipoOportunidade, Oportunidade
#from .forms import OportunidadeForm
#from empresa.models import Empresa
from questionario.models import Questionario, RespostaQuestionario
from egresso.models import Egresso, Endereco, Formacao, obter_egresso
#from curso.models import Curso, AreaAtuacao, NivelCurso
#from account.models import User


@require_http_methods(["GET", "POST"])
@is_user('egresso')
def questionarios(request, mensagem=None):
    egresso = obter_egresso(user=request.user)
    formacoes = egresso.find_formacoes(curso__is_local= True)

    data = {'formacoes': [f.as_dict() for f in formacoes]}

    print(data, request.GET)
    return render(request, 'questionario/questionarios_curso.html', data)


@require_http_methods(["GET", "POST"])
@is_user('egresso')
@csrf_exempt
def responder_questionario(request, quest_id, formacao_id):
    egresso = obter_egresso(user=request.user)
    formacao = get_object_or_404(Formacao, pk=formacao_id, egresso__pk=egresso.id)
    quest = get_object_or_404(Questionario, pk=quest_id)

    data = {
        'questionario': quest.as_dict(),
        'formacao': formacao.as_dict(),
    }
    
    if formacao.questionario_foi_respondido(quest_id):
        return HttpResponseRedirect(reverse('questionario:listar-todos'))

    if request.method == "GET":
        return render(request, 'questionario/responder.html', data)
        
    for questao_id, resp in dict(request.POST).items():
        resposta = RespostaQuestionario()        
        resposta.formacao = formacao
        resposta.questao_id = questao_id
        resposta.questionario_id = quest_id
        resposta.resposta = ' '.join(resp)
        resposta.save()

    return HttpResponseRedirect(reverse('questionario:listar-todos'))

