from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.admin import site as admin_site
from django.template.response import TemplateResponse


@never_cache
def index_admin(request, extra_context=None):
    """
    Display the main admin index page, which lists all of the installed
    apps that have been registered in this site.
    """

    APPS_EXIBIR = {
        'Account': ['User'],
        'Curso': ['Curso', 'Nivel_Curso'],
        'Egresso': ['Egresso', 'Formacao_Academica'],
        'Empresa': ['Empresa'],
        'Oportunidade': ['Oportunidade']
    }

    app_list = admin_site.get_app_list(request)
    app_list = [app for app in app_list if app['name'] in APPS_EXIBIR]
    
    for app in app_list:
        app_name = app['name']
        app['models'] = [m for m in app['models'] if m['object_name'] in APPS_EXIBIR[app_name]]       

    context = {
        **admin_site.each_context(request),
        'title': admin_site.index_title,
        'app_list': app_list,
        **(extra_context or {}),
    }

    request.current_app = admin_site.name

    return TemplateResponse(request, 'admin/index.html', context)

