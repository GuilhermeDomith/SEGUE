from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods

from .models import Empresa, Area_Atuacao_Empresa
from .forms import EmpresaForm
from egresso.models import Egresso, Endereco, Formacao_Academica
from curso.models import Curso, Area_Curso, Nivel_Curso
from oportunidade.models import Tipo_Oportunidade, Oportunidade
from account.models import User
from SEGUE.decorators import is_user



@require_http_methods(["GET", "POST"])
@is_user('empresa')
def editar_dados(request):

    data = {'areas_atuacao': Area_Atuacao_Empresa.objects.values()}
    user = User.objects.get(email=request.user.email)
    empresa = Empresa.get_empresa_user(user)

    if request.method == "GET":
        if empresa:
            data.update({'form': EmpresaForm(empresa.__dict__)})

        return render(request, 'empresa/dados_empresa.html', data)

    form = EmpresaForm(request.POST)
    if not form.is_valid():
        data.update({'form': form})
        return render(request, 'empresa/dados_empresa.html', data)

    form.save()
    return HttpResponseRedirect("/")


############

@require_http_methods(["GET"])
@is_user('empresa')
def oportunidades_lancadas(request):
    user = User.objects.get(email=request.user.email)
    empresa = Empresa.get_empresa_user(request.user)
    oportunidades = empresa.get_oportunidades() if empresa else []

    print(oportunidades)
    data = {'oportunidades':[]}
    for o in oportunidades:
        oport_dict = o.as_dict()
        formacoes = Formacao_Academica.get_formacoes(
            curso_id= o.curso_necessario_id, 
            nivel_formacao= o.nivel_formacao
        )

        oport_dict['egressos'] = [ f.egresso.as_dict() for f in formacoes]
        data['oportunidades'].append(oport_dict)

    data['empresa'] = empresa.as_dict()
    return render(request, 'empresa/oportunidades_lancadas.html', data)

############

@require_http_methods(["POST"])
@is_user('empresa')
def enviar_email_egresso(request):

    print(request.POST)
    return HttpResponseRedirect(reverse('empresa:oportunidades'))
    send_mail(
        'Teste de email do django',
        'Estou testando o envio de email, apenas isso',
        'guilhermedomith@hotmail.com',
        ['guilhermedomith@gmail.com'],
        fail_silently=False,
    )

    return HttpResponseRedirect(reverse('empresa:oportunidades'))

