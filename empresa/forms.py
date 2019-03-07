from django import forms
from SEGUE import settings
from .models import Empresa

class EmpresaForm(forms.Form):
    razao_social = forms.CharField(max_length=100)
    cnpj = forms.CharField(max_length=18)
    email = forms.CharField(max_length=255)
    telefone = forms.CharField(max_length=20)
    area_atuacao_id = forms.IntegerField(required=False)

class OportunidadeForm(forms.Form):
    id = forms.IntegerField(required=False)
    nivel_formacao_id = forms.IntegerField(error_messages={'required': 'Selecione o nível do curso'})
    curso_necessario_id = forms.IntegerField(error_messages={'required': 'Selecione o nome do curso'})
    tipo_id = forms.IntegerField(error_messages={'required': 'Selecione o tipo de oportunidade a ser oferecida'})
    horas_semana = forms.IntegerField()
    titulo = forms.CharField(max_length=50)
    cidade = forms.CharField(max_length=60)
    estado = forms.CharField(max_length=2)


