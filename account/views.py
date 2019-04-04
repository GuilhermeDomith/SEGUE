from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url



class MyLoginView(LoginView):

    '''@method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)'''

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