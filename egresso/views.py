from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta

from .models import Egresso, Endereco, Formacao_Academica
from .forms import EgressoForm, FormacaoForm
from oportunidade.models import Oportunidade
from curso.models import Curso, Area_Curso, Nivel_Curso
from account.models import User
from SEGUE.decorators import is_user


def obter_dados_pag_curriculo(request, codigo=None):
	""" Se nenhum código for fornecido é obtido os dados do usuário logado (Egresso)"""

	if not codigo:
		user = User.objects.get(email=request.user.email)
		egresso = Egresso.get_egresso_user(user)
	else:
		egresso = Egresso.objects.get(pk=codigo)
		user = egresso.user

	formacoes = None

	if egresso:
		egresso_dict = egresso.as_dict()
		formacoes =[f.as_dict() for f in egresso.get_formacoes()]

	data = {
		'egresso': egresso_dict if egresso else {},
		'niveis_curso': Nivel_Curso.objects.values(),
		'cursos': Curso.objects.values(),
		'areas_curso': Area_Curso.objects.values(),
		'formacoes_escolares': formacoes if formacoes else []
	}

	return data, user, egresso

############ Views ############

@require_http_methods(["GET", "POST"])
@is_user('egresso')
def editar_meu_curriculo(request):
	user = User.objects.get(email=request.user.email)
	egresso = Egresso.get_egresso_user(request.user)

	if request.method == 'GET':
		data = {}
		# Se existe egresso associado ao usuário, obtém os dados
		if egresso:
			dict_form = egresso.as_dict()
			data.update({'form': EgressoForm(dict_form)})
		return render(request, 'egresso/editar_curriculo.html', data)

	form = EgressoForm(request.POST)
	if not form.is_valid():
		return render(request, 'egresso/editar_curriculo.html', {'form': form})
	
	print(form.cleaned_data)
	form.save()
	return HttpResponseRedirect(reverse('egresso:meu-curriculo'))

############

@require_http_methods(["GET"])
@is_user('egresso')
def meu_curriculo(request):
	data, _, _ = obter_dados_pag_curriculo(request)
	data['modo_edicao'] = True
	return render(request, 'egresso/curriculo.html', data)


############

@require_http_methods(["GET"])
@is_user('egresso')
def ver_curriculo(request, codigo):
	data, _, _ = obter_dados_pag_curriculo(request, codigo)
	return render(request, 'egresso/curriculo.html', data)

############

@require_http_methods(["POST"])
@is_user('egresso')
def adicionar_formacao(request):
	data, _, _ = obter_dados_pag_curriculo(request)

	form = FormacaoForm(request.POST)
	if not form.is_valid():
		data.update({'form': form, 'open_formacao': 'true'})
		return render(request, 'egresso/curriculo.html', data)

	form.save()
	return HttpResponseRedirect(reverse('egresso:meu-curriculo'))

############

@require_http_methods(["GET"])
@is_user('egresso')
def excluir_formacao(request, id):
	egresso = Egresso.get_egresso_user(request.user)

	try:
		formacao = egresso.formacao_academica_set.get(pk=id)
		formacao.delete()
	except Formacao_Academica.DoesNotExist:
		pass

	return HttpResponseRedirect(reverse('egresso:meu-curriculo'))


############

@require_http_methods(["GET"])
@is_user('egresso')
def oportunidades(request):
	user = User.objects.get(email=request.user.email)
	egresso = Egresso.get_egresso_user(user)
	oportunidades = []

	print(egresso)

	if egresso:
		for f in egresso.formacao_academica_set.all():
			oport = Oportunidade.get_oportunidades(
				curso_necessario=f.curso,
				nivel_formacao=f.nivel_formacao
			)

			oportunidades += [o.as_dict() for o in oport]

	data = {'egresso': egresso.as_dict()}	
	data.update({'oportunidades': oportunidades})
	return render(request, 'egresso/oportunidades.html', data)



