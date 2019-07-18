from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods

from .models import TipoOportunidade, Oportunidade
from .forms import OportunidadeForm
from empresa.models import Empresa, obter_empresa
from egresso.models import Egresso, Endereco, Formacao
from curso.models import Curso, AreaAtuacao, NivelCurso
from account.models import User
from SEGUE.decorators import is_user



@require_http_methods(["GET", "POST"])
@is_user('empresa')
def adicionar_oportunidade(request, codigo=None):
    user = User.objects.get(username=request.user.username)
    empresa = obter_empresa(user=request.user)

    data = {
        'niveis_curso': NivelCurso.objects.values(),
		'cursos': Curso.objects.values(),
        'tipos_oportunidade': TipoOportunidade.objects.values(),
        'empresa': empresa 
	}

    if request.method == "GET":
        if codigo:
            oportunidade = Oportunidade.objects.get(pk=codigo)
            form = OportunidadeForm(oportunidade.__dict__)
            data.update({'form': form})
        
        return render(request, 'empresa/add_oportunidade.html', data)

    form = OportunidadeForm(request.POST)
    if not form.is_valid():
        data.update({'form': form})
        return render(request, 'empresa/add_oportunidade.html', data)

    form.save()    
    return HttpResponseRedirect(reverse('empresa:oportunidades'))


############

@require_http_methods(["GET", "POST"])
@is_user('empresa')
def excluir_oportunidade(request, codigo):
    empresa = obter_empresa(user=request.user)
    oportunidade = empresa.oportunidade_set.get(pk=codigo)
    oportunidade.delete()
    return HttpResponseRedirect(reverse('empresa:oportunidades'))
