from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [    
    path('dados/', views.editar_dados, name='editar-dados'),
    path('oportunidades/', views.oportunidades_lancadas, name='oportunidades'),
    path('email_egresso/', views.enviar_email_egresso, name='email_egresso')
]

