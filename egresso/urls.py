from django.urls import path
from . import views

app_name = 'egresso'

urlpatterns = [    
    path('meu-curriculo/', views.editar_meu_curriculo, name='editar-curriculo'),
    path('<int:codigo>/', views.info_egresso, name='info'), 
]

