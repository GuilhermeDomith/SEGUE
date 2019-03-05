from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from egresso.models import Egresso, Endereco, Nivel_Formacao, Curso, Area_Curso, Formacao_Escolar
from .models import Empresa, Area_Atuacao_Empresa
from .forms import EmpresaForm
import json


def eh_empresa(user):
    return user.groups.filter(name='empresa').exists()

############ Views ############

@require_http_methods(["GET", "POST"])
@login_required
@user_passes_test(eh_empresa, login_url='/', redirect_field_name=None)
def editar_dados(request):

    data = {'areas_atuacao': Area_Atuacao_Empresa.objects.values()}
    user = User.objects.get(username=request.user.username)
    empresa = Empresa.get_empresa_user(user)

    if request.method == "GET":
        empresa_dict = empresa.__dict__ if empresa else {}
        empresa_dict['email'] = user.email    
        data.update({'form': EmpresaForm(empresa_dict)})
        return render(request, 'empresa/dados.html', data)

    form = EmpresaForm(request.POST)
    if not form.is_valid():
        data.update({'form': form})
        return render(request, 'empresa/dados.html', data)

    empresa_dict = form.cleaned_data.copy()
    del empresa_dict['email']

    empresa = Empresa(
        pk=empresa.pk if empresa else None,
        user = user,
        **empresa_dict        
    )
    empresa.save()

    user.email = form.cleaned_data['email']
    user.save()
    return HttpResponseRedirect("/")


############


@require_http_methods(["GET"])
@login_required
@user_passes_test(eh_empresa, login_url='/', redirect_field_name=None)
def oportunidades_lancadas():
    return HttpResponseRedirect(reverse('egresso:curriculo'))
