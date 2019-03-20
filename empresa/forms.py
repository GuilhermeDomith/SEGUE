from django import forms
from SEGUE import settings
from .models import Empresa
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



