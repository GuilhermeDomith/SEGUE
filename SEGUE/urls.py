from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('egresso/', include('egresso.urls')),
    path('empresa/', include('empresa.urls')),
    #path('curso/', include('curso.urls')),
    path('oportunidade/', include('oportunidade.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
