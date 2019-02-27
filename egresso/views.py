from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from .models import Egresso
from .forms import EgressoForm



@login_required
@user_passes_test(lambda u: eh_membro_grupo(u, 'egresso'), login_url='/', redirect_field_name=None)
def editar_meu_curriculo(request):
    '''
        @require_role('admin')


        Esta view retorna a página para edição do currículo do egresso no caso de uma requisição GET.
        Para uma requisição POST a view irá salvar os dados enviados do engresso e irá redirecionar 
        para a página inicial.

        DECORATOR user_passes_test: Se o usuário não for membro do grupo 'egresso', logo ele não terá um 
        currículo e será redirecionado para a página inicial. O parâmetro redirect_field_name igual 
        a None indica que não será usado a função 'next'.
    '''
    if request.method == 'GET':
        try:
            egresso = request.user.egresso
        except Egresso.DoesNotExist as e:
            egresso = Egresso(user = request.user)
            egresso.save()
            print('egresso salvo')

        form = EgressoForm(egresso.__dict__)
        return render(request, 'egresso/editar_curriculo.html', {'form': form})

    print(request.POST)

    form = EgressoForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        return render(request, 'index.html')
    else:
        print(form.errors)
        return render(request, 'egresso/editar_curriculo.html', {'form': form})


def info_egresso(codigo):
    pass

def eh_membro_grupo(user, nome_grupo):
    return user.groups.filter(name=nome_grupo).exists()
