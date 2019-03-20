from django import forms
from SEGUE import settings
from .models import Oportunidade
from account.models import User

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