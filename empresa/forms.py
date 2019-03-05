from django import forms
from SEGUE import settings
from .models import Empresa

class EmpresaForm(forms.Form):
    razao_social = forms.CharField(max_length=100)
    cnpj = forms.CharField(max_length=18)
    email = forms.CharField(max_length=255)
    telefone = forms.CharField(max_length=20)
    area_atuacao_id = forms.IntegerField(required=False)


