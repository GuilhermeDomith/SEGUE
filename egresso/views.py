from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Egresso, Endereco
from .forms import EgressoForm
import json



@login_required
@user_passes_test(lambda u: eh_membro_grupo(u, 'egresso'), login_url='/', redirect_field_name=None)
def editar_meu_curriculo(request):
    '''
        Esta view retorna a página para edição do currículo do egresso no caso de uma requisição GET.
        Para uma requisição POST a view irá salvar os dados enviados do engresso e irá redirecionar 
        para a página inicial.

        DECORATOR user_passes_test: Se o usuário não for membro do grupo 'egresso', logo ele não terá um 
        currículo e será redirecionado para a página inicial. O parâmetro redirect_field_name igual 
        a None indica que não será usado a função 'next'.
    '''

    user = User.objects.get(username=request.user.username)

    egresso = None
    try: egresso = request.user.egresso
    except Egresso.DoesNotExist:pass

    
    endereco = None
    try:
        if egresso: 
            endereco = egresso.endereco
    except Egresso.DoesNotExist:
        pass

    if request.method == 'GET':
        # Verifica se existe egresso já associado ao usuário.
        if egresso:
            dict_form = egresso.__dict__
            if endereco:
                dict_form.update(endereco.__dict__)

            form = EgressoForm(dict_form)
            return render(request, 'egresso/editar_curriculo.html', {'form': form})    
        else:
            return render(request, 'egresso/editar_curriculo.html', {'form': EgressoForm()})
        

    form = EgressoForm(request.POST)
    if form.is_valid():
        if egresso:
            egresso.matricula = form.cleaned_data['matricula']
            print('ssssss')
        else:
            egresso = Egresso(
                **Egresso.form_to_dict(form.cleaned_data), 
                user= user
            )

            endereco = Endereco(
                **Endereco.form_to_dict(form.cleaned_data), 
            )


        print(egresso.__dict__)
        endereco.save()
        egresso.endereco = endereco
        egresso.save()
        return render(request, 'index.html')
    else:
        return render(request, 'egresso/editar_curriculo.html', {'form': form})


def info_egresso(codigo):
    pass

def eh_membro_grupo(user, nome_grupo):
    return user.groups.filter(name=nome_grupo).exists()
