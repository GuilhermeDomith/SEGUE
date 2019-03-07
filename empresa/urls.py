from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [    
    path('oportunidades/', views.oportunidades_lancadas, name='oportunidades'),
    path('dados/', views.editar_dados, name='editar-dados'),
    path('oportunidade/', views.adicionar_oportunidade, name='add-oportunidade'),
    path('oportunidade/<int:codigo>', views.adicionar_oportunidade, name='editar-oportunidade'),
    path('oportunidade/<int:codigo>/del', views.excluir_oportunidade, name='del-oportunidade'),
]

