from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url



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
