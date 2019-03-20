from django.urls import path
from . import views

app_name = 'oportunidade'

urlpatterns = [    
    path('', views.adicionar_oportunidade, name='add'),
    path('<int:codigo>', views.adicionar_oportunidade, name='editar'),
    path('<int:codigo>/del', views.excluir_oportunidade, name='delete'),
]

