from django.urls import path
from . import views

app_name = 'egresso'

urlpatterns = [    
    path('meu-curriculo/', views.meu_curriculo, name='curriculo'),
    path('meu-curriculo/editar/', views.editar_meu_curriculo, name='editar-curriculo'),
    path('meu-curriculo/formacao/add', views.adicionar_formacao, name='add-formacao'),
    path('meu-curriculo/formacao/<int:id>/del', views.excluir_formacao, name='excluir-formacao'),
    path('oportunidades/', views.oportunidades, name='oportunidades') 
]

