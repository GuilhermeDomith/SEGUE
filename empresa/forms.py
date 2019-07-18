from django import forms
from SEGUE import settings
from .models import Empresa
from account.models import User

class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ['razao_social', 'cnpj', 'telefone']

    id = forms.IntegerField(required=False)
    user_id = forms.IntegerField()
    #razao_social = forms.CharField(max_length=100)
    #cnpj = forms.CharField(max_length=18)
    #telefone = forms.CharField(max_length=20)

    def save(self, commit=True):
        empresa = Empresa(**self.cleaned_data)
        print('AQUI: \n\n', self.cleaned_data)
        if commit:
            empresa.save()

        return empresa



