from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.http import require_http_methods
from SEGUE.decorators import is_user

#from .models import TipoOportunidade, Oportunidade
#from .forms import OportunidadeForm
#from empresa.models import Empresa
from egresso.models import Egresso, Endereco, Formacao, obter_egresso
#from curso.models import Curso, AreaAtuacao, NivelCurso
#from account.models import User


@require_http_methods(["GET", "POST"])
@is_user('egresso')
def questionario(request, id):
    data = {
        'titulo': f'Questionario de {id} Anos'
    }
    return render(request, 'questionario/responder.html', data)


@require_http_methods(["GET", "POST"])
@is_user('egresso')
def questionarios(request):
    egresso = obter_egresso(user=request.user)
    formacoes = egresso.find_formacoes(curso__is_local= True)
    print(formacoes)
    return render(request, 'questionario/questionarios_curso.html')