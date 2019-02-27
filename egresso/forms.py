from django import forms
from SEGUE import settings
from .models import Egresso, Endereco

class EgressoForm(forms.Form):
    matricula = forms.CharField(max_length=30)
    nome_completo = forms.CharField(help_text=100)  
    data_nascimento = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    cpf = forms.CharField(max_length=15, required=False)
    identidade = forms.CharField(max_length=15, required=False)

    link_likedin = forms.CharField(max_length=250, required=False)
    link_lattes = forms.CharField(max_length=250, required=False)
    link_github = forms.CharField(max_length=250, required=False)

    cep = forms.CharField(max_length=15, required=False)
    rua = forms.CharField(max_length=150)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=20, required=False)
    bairro = forms.CharField(max_length=60, required=False)
    cidade = forms.CharField(max_length=60)
    estado = forms.CharField(max_length=2)

    def clean(self):
        cleaned_data = super(EgressoForm, self).clean()
        print('cleannnnnnnnnnnnnn', cleaned_data)
        '''
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')'''

        #if not name and not email and not message:
            #raise forms.ValidationError('You have to write something!')

        return cleaned_data

    def clean_data_nascimento(self):
        return '2014-02-27'
