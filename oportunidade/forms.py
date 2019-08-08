from django import forms
from SEGUE import settings
from .models import Oportunidade
from account.models import User

class OportunidadeForm(forms.ModelForm):

    class Meta:
        model = Oportunidade
        exclude = ['empresa', 'nivel_formacao', 'area_necessaria', 'nivel_necessario', 'tipo']
        fields = ['estado', 'cidade', 'horas_semana', 'titulo']

    id = forms.IntegerField(required=False)
    empresa_id = forms.IntegerField()
    tipo_id = forms.IntegerField(error_messages={'required': 'Selecione o tipo de oportunidade a ser oferecida'})
    nivel_necessario_id = forms.IntegerField(error_messages={'required': 'Selecione o nível do curso'})
    area_necessaria_id = forms.IntegerField(error_messages={'required': 'Selecione pelo menos uma área necessária'})

    def save(self, commit=True):
        oportunidade = Oportunidade(**self.cleaned_data)

        if commit:
            oportunidade.save()
        return oportunidade