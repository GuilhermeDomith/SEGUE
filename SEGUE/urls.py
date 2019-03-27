from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from account.views import base_layout

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('egresso/', include('egresso.urls')),
    path('empresa/', include('empresa.urls')),
    #path('curso/', include('curso.urls')),
    path('oportunidade/', include('oportunidade.urls')),

    path('base_layout/', base_layout, name='base_layout'), 
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
