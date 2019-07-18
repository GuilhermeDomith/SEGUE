from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', include('pwaconfig.urls')),
    path('', include('account.urls')),
    path('', include('custom_admin.urls')),
    path('admin/', admin.site.urls),
    path('egresso/', include('egresso.urls')),
    path('questionario/', include('questionario.urls')),
    path('empresa/', include('empresa.urls')),
    #path('curso/', include('curso.urls')),
    path('oportunidade/', include('oportunidade.urls')),
    
    path('', views.index),
]
