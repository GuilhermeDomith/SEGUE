from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from django.views.generic.edit import CreateView 

from .models import Egresso, Endereco, Formacao, obter_egresso, obter_formacoes
from .forms import FormacaoForm, DadosPessoaisForm, EnderecoForm
from oportunidade.models import Oportunidade, obter_oportunidades
from curso.models import Curso, AreaAtuacao, NivelCurso
from account.models import User
from SEGUE.decorators import is_user


############ Views ############

@require_http_methods(["GET", "POST"])
@is_user('egresso')
def dados_pessoais(request):
	egresso = obter_egresso(user=request.user)
	data = {'egresso': egresso.as_dict()}

	if request.method == 'GET':
		if data['egresso']['dados']:
			data['egresso']['dados'].update(egresso_id=egresso.pk)
			
			form = DadosPessoaisForm(
				data['egresso']['dados'],
			)
			data.update({'form': form})
		return render(request, 'egresso/dados_pessoais.html', data)

	form = DadosPessoaisForm(request.POST)
	if not form.is_valid():
		data.update({'form': form})
		return render(request, 'egresso/dados_pessoais.html', data)
	
	form.save()
	return HttpResponseRedirect(reverse('egresso:meu-curriculo'))

############

@require_http_methods(["GET", "POST"])
@is_user('egresso')
def endereco(request):
	egresso = obter_egresso(user=request.user)
	data = {'egresso': egresso.as_dict()}

	if request.method == 'GET':
		endereco_dict = data['egresso']['endereco']
		if endereco_dict:
			data.update({'form': EnderecoForm(endereco_dict)})
		return render(request, 'egresso/endereco.html', data)

	form = EnderecoForm(request.POST)
	if not form.is_valid():
		data.update({'form': form})
		return render(request, 'egresso/endereco.html', data)
	
	form.save()
	return HttpResponseRedirect(reverse('egresso:meu-curriculo'))

############

@require_http_methods(["GET"])
@is_user('egresso')
def meu_curriculo(request):
	egresso = obter_egresso(user=request.user)
	questionarios = egresso.questionarios_para_responder()

	cont = 0
	for q in questionarios:
		cont += len(q['responder'])

	data = {
		'n_quest': cont,
		'egresso': egresso.as_dict(),
		'formacoes_escolares': egresso.get_formacoes_dict()
	}

	data['modo_edicao'] = True
	return render(request, 'egresso/curriculo.html', data)


############

@require_http_methods(["GET"])
@is_user('empresa')
def ver_curriculo(request, codigo):
	egresso = obter_egresso(pk=codigo)

	data = {
		'egresso': egresso.as_dict(),
		'formacoes_escolares': egresso.get_formacoes_dict()
	}

	data['modo_edicao'] = False
	return render(request, 'egresso/curriculo.html', data)

############

@require_http_methods(["GET", "POST"])
@is_user('egresso')
def adicionar_formacao(request):
	user = User.objects.get(username=request.user.username)
	egresso = obter_egresso(user=request.user)
	data = {'egresso': egresso.as_dict()}

	if request.method == "GET":
		form = FormacaoForm()
		data.update({'form': form})
		return render(request, 'egresso/formacao.html', data)

	form = FormacaoForm(request.POST)
	if not form.is_valid():
		data.update({'form': form})
		return render(request, 'egresso/formacao.html', data)

	form.save()    
	return HttpResponseRedirect(reverse('egresso:meu-curriculo'))

############

@require_http_methods(["GET"])
@is_user('egresso')
def excluir_formacao(request, id):
	egresso = obter_egresso(user=request.user)

	try:
		formacao = egresso.formacao_set.get(pk=id)
		formacao.delete()
	except Formacao.DoesNotExist:
		pass

	return HttpResponseRedirect(reverse('egresso:meu-curriculo'))


############

@require_http_methods(["GET"])
@is_user('egresso')
def oportunidades(request):
	egresso = obter_egresso(user=request.user)
	oportunidades = []

	if egresso:
		for f in egresso.get_formacoes():
			oport = obter_oportunidades(
				area_necessaria=f.curso.area_atuacao,
				nivel_necessario=f.curso.nivel_curso
			)

			oportunidades += [o.as_dict() for o in oport]

	data = {'egresso': egresso.as_dict()}	
	data.update({'oportunidades': oportunidades})
	return render(request, 'egresso/oportunidades.html', data)



