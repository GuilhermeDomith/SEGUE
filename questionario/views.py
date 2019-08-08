from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from django.views.decorators.http import require_http_methods
from SEGUE.decorators import is_user

#from .models import TipoOportunidade, Oportunidade
#from .forms import OportunidadeForm
#from empresa.models import Empresa
from questionario.models import Questionario
from egresso.models import Egresso, Endereco, Formacao, obter_egresso
#from curso.models import Curso, AreaAtuacao, NivelCurso
#from account.models import User


@require_http_methods(["GET", "POST"])
@is_user('egresso')
def questionarios(request):
    egresso = obter_egresso(user=request.user)
    formacoes = egresso.find_formacoes(curso__is_local= True)
    data = {
        'formacoes': [f.as_dict() for f in formacoes]
    }
    print(data)
    return render(request, 'questionario/questionarios_curso.html', data)


@require_http_methods(["GET", "POST"])
@is_user('egresso')
def questionario(request, quest_id, formacao_id):
    egresso = obter_egresso(user=request.user)
    formacao = get_object_or_404(Formacao, pk=formacao_id, egresso__pk=egresso.id)
    quest = get_object_or_404(Questionario, pk=quest_id)
    
    if formacao.questionario_foi_respondido(quest_id):
        return questionarios(request)

    data = {
        'questionario': quest.as_dict(),
        'formacao': formacao.as_dict(),
    }

    return render(request, 'questionario/responder.html', data)
