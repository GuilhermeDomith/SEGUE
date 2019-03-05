from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import Egresso, Endereco, Nivel_Formacao, Curso, Area_Curso, Formacao_Escolar
from .forms import EgressoForm, FormacaoForm
from datetime import datetime, timedelta
import json


def eh_egresso(user):
    return user.groups.filter(name='egresso').exists()


def obter_dados_pag_curriculo(request):
	user = User.objects.get(username=request.user.username)
	egresso = Egresso.get_egresso_user(request.user)
	formacoes = None

	if egresso:
		egresso_dict = egresso.__dict__
		egresso_dict.update({'idade':egresso.get_idade()})
		formacoes =[f.get_form_detalhado() for f in egresso.get_formacoes()]

	data = {
		'egresso': egresso_dict if egresso else {},
		'niveis_curso': Nivel_Formacao.objects.values(),
		'cursos': Curso.objects.values(),
		'areas_curso': Area_Curso.objects.values(),
		'formacoes_escolares': formacoes if formacoes else []
	}

	return data, user, egresso

############ Views ############

@require_http_methods(["GET", "POST"])
@login_required
@user_passes_test(eh_egresso, login_url='/', redirect_field_name=None)
def editar_meu_curriculo(request):
	user = User.objects.get(username=request.user.username)
	egresso = Egresso.get_egresso_user(request.user)
	endereco = egresso.get_endereco() if egresso else None

	if request.method == 'GET':
		form = EgressoForm()

		# Se existe egresso associado ao usuário, obtém os dados
		if egresso:
			dict_form = egresso.__dict__
			dict_form.update(endereco.__dict__ if endereco else '')
			form = EgressoForm(dict_form)

		return render(request, 'egresso/editar_curriculo.html', {'form': form})

	form = EgressoForm(request.POST)
	if not form.is_valid():
		return render(request, 'egresso/editar_curriculo.html', {'form': form})

	# Obtém o endereço a ser adicionado ou editado
	endereco_update = Endereco(**Endereco.form_to_dict(form.cleaned_data))
	endereco_update.pk = endereco.pk if endereco else None
	endereco_update.save()

	# Obtém o egresso a ser adicionado ou editado
	egresso_update = Egresso(
		**Egresso.form_to_dict(form.cleaned_data),
		user=user,
		endereco=endereco_update,
	)
	egresso_update.pk = egresso.pk if egresso else None
	egresso_update.save()

	return HttpResponseRedirect(reverse('egresso:curriculo'))

############

@require_http_methods(["GET"])
@login_required
@user_passes_test(eh_egresso, login_url='/', redirect_field_name=None)
def meu_curriculo(request):
	data, user, egresso = obter_dados_pag_curriculo(request)
	return render(request, 'egresso/curriculo.html', data)

############

@require_http_methods(["POST"])
@login_required
@user_passes_test(eh_egresso, login_url='/', redirect_field_name=None)
def adicionar_formacao(request):
	data, user, egresso = obter_dados_pag_curriculo(request)

	form = FormacaoForm(request.POST)
	if not form.is_valid():
		data.update({'form': form, 'open_modal': 'true'})
		return render(request, 'egresso/curriculo.html', data)

	if not egresso:
		egresso = Egresso(user=user)
		egresso.save()

	# Cria a formação a ser adicionada
	formacao = Formacao_Escolar(
		egresso=egresso,
		**Formacao_Escolar.form_to_dict(form.cleaned_data)
	)

	formacao.save()
	return HttpResponseRedirect(reverse('egresso:curriculo'))

############

@require_http_methods(["GET"])
@login_required
@user_passes_test(eh_egresso, login_url='/', redirect_field_name=None)
def excluir_formacao(request, id):
	egresso = Egresso.get_egresso_user(request.user)

	try:
		formacao = egresso.formacao_escolar_set.get(pk=id)
		formacao.delete()
	except Formacao_Escolar.DoesNotExist:
		pass

	return HttpResponseRedirect(reverse('egresso:curriculo'))


############

@require_http_methods(["GET"])
@login_required
@user_passes_test(eh_egresso, login_url='/', redirect_field_name=None)
def oportunidades():
	return HttpResponseRedirect(reverse('egresso:curriculo'))



