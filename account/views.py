from django.conf import settings
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, resolve_url
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_http_methods
from .forms import EgressoForm



class MyLoginView(LoginView):
        
    redirect_authenticated_user = True

    def get_success_url(self):
        url = self.get_redirect_url()
        user = self.request.user

        if user.is_tipo('admin'):
            url = '/admin/'
        elif user.is_tipo('egresso'):
            url = '/egresso/oportunidades'
        elif user.is_tipo('empresa'):
            url = '/empresa/oportunidades'

        return url or resolve_url(settings.LOGIN_REDIRECT_URL)


@require_http_methods(["GET", "POST"])
def cadastrar_se(request):
    data = {}

    if request.method == 'GET':
        form = EgressoForm()
        data.update({'form': form})
        return render(request, 'registration/sign-up.html', data)

    form = EgressoForm(request.POST)
    if not form.is_valid():
        data.update({'form': form})
        return render(request, 'registration/sign-up.html', data)

    form.save()
    return HttpResponseRedirect(reverse('account:login'))
