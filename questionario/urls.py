from django.urls import path
from . import views

app_name = 'questionario'

urlpatterns = [    
    path('', views.questionarios, name='listar-todos'),
    path('<int:quest_id>/curso/<int:formacao_id>', views.questionario, name='responder'),
]

