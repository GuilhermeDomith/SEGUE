from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [    
    path('serviceworker.js', views.service_worker),
    path('manifest.json', views.manifest),
]
