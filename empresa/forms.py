from django import forms
from SEGUE import settings
from .models import Empresa, Oportunidade
from account.models import User

class EmpresaForm(forms.Form):
    id = forms.IntegerField(required=False)
    user_id = forms.IntegerField()
    razao_social = forms.CharField(max_length=100)
    cnpj = forms.CharField(max_length=18)
    telefone = forms.CharField(max_length=20)
    area_atuacao_id = forms.IntegerField(required=False)

    def save(self, commit=True):
        empresa = Empresa(**self.cleaned_data)

        if commit:
            empresa.save()

        return empresa

class OportunidadeForm(forms.Form):
    id = forms.IntegerField(required=False)
    empresa_id = forms.IntegerField()
    nivel_formacao_id = forms.IntegerField(error_messages={'required': 'Selecione o nível do curso'})
    curso_necessario_id = forms.IntegerField(error_messages={'required': 'Selecione o nome do curso'})
    tipo_id = forms.IntegerField(error_messages={'required': 'Selecione o tipo de oportunidade a ser oferecida'})
    horas_semana = forms.IntegerField()
    titulo = forms.CharField(max_length=50)
    cidade = forms.CharField(max_length=60)
    estado = forms.CharField(max_length=2)

    def save(self, commit=True):
        oportunidade = Oportunidade(**self.cleaned_data)

        if commit:
            oportunidade.save()
        return oportunidade


