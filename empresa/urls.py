from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [    
    path('oportunidades/', views.oportunidades_lancadas, name='oportunidades'),
]

