from django.urls import path
from . import views

app_name = 'egresso'

urlpatterns = [    
    path('', views.meu_curriculo, name='meu-curriculo'),
    path('dados-pessoais/', views.dados_pessoais, name='dados-pessoais'),
    path('endereco/', views.endereco, name='endereco'),
    path('formacao/add', views.adicionar_formacao, name='add-formacao'),
    path('formacao/<int:id>/del', views.excluir_formacao, name='excluir-formacao'),
    path('oportunidades/', views.oportunidades, name='oportunidades'),
    path('<int:codigo>/', views.ver_curriculo, name='curriculo') 

]

