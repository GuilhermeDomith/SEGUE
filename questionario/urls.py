from django.urls import path
from . import views

app_name = 'questionario'

urlpatterns = [    
    path('', views.questionarios, name='listar-todos'),
    path('<int:id>', views.questionario, name='responder'),
]

