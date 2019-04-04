from django.urls import path
from . import views

app_name='custom_admin'

urlpatterns = [   
    path('admin/', views.index_admin, name='index'), 
]