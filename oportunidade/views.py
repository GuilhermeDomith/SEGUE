from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods

from .models import Tipo_Oportunidade, Oportunidade
from empresa.models import Empresa, Area_Atuacao_Empresa
from egresso.models import Egresso, Endereco, Formacao_Academica
from curso.models import Curso, Area_Curso, Nivel_Curso
from account.models import User
from .forms import OportunidadeForm



@require_http_methods(["GET", "POST"])
@login_required
@user_passes_test(lambda u: u.is_tipo('empresa'), login_url='/', redirect_field_name=None)
def adicionar_oportunidade(request, codigo=None):
    user = User.objects.get(username=request.user.username)
    empresa = Empresa.get_empresa_user(request.user)

    data = {
        'niveis_curso': Nivel_Curso.objects.values(),
		'cursos': Curso.objects.values(),
        'tipos_oportunidade': Tipo_Oportunidade.objects.values(),
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
@login_required
@user_passes_test(lambda u: u.is_tipo('empresa'), login_url='/', redirect_field_name=None)
def excluir_oportunidade(request, codigo):
    empresa = Empresa.get_empresa_user(request.user)
    oportunidade = empresa.oportunidade_set.get(pk=codigo)
    oportunidade.delete()
    return HttpResponseRedirect(reverse('empresa:oportunidades'))
