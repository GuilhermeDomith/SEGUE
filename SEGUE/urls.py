from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
<<<<<<< HEAD
from django.contrib.auth import views as auth_views
from account.views import base_layout

urlpatterns = [
    path('', include('pwa.urls')),
=======

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),

    path('', include('account.urls')),
    path('', include('custom_admin.urls')),
>>>>>>> e5edae091456559c11c836c9bcb4eb7b33d73a3d
    path('admin/', admin.site.urls),
    path('egresso/', include('egresso.urls')),
    path('empresa/', include('empresa.urls')),
    #path('curso/', include('curso.urls')),
    path('oportunidade/', include('oportunidade.urls')),
<<<<<<< HEAD

    path('', TemplateView.as_view(template_name='index.html')),
    path('base_layout/', base_layout, name='base_layout'), 
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
=======
>>>>>>> e5edae091456559c11c836c9bcb4eb7b33d73a3d
]
