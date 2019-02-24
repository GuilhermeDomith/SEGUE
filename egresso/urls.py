from django.urls import path
from . import views

app_name = 'egresso'

urlpatterns = [    
    path('cadastro/', views.cadastro_egresso, name='cadastro'),
    path('<int:codigo>/', views.info_egresso, name='info'), 
]

