from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
    # Se logado, redireciona para que a página de login
    # e assim o usuário será redirecionado de acordo com tipo usuário.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('account:login'))    
        
    return render(request, 'index.html')