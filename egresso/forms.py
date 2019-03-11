from django import forms
from SEGUE import settings
from .models import Egresso, Endereco
import re

class EgressoForm(forms.Form):
    id = forms.IntegerField(required=False)
    matricula = forms.CharField(max_length=30)
    nome_completo = forms.CharField(help_text=100)  
    data_nascimento = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    cpf = forms.CharField(max_length=15, required=False)
    identidade = forms.CharField(max_length=15, required=False)

    link_linkedin = forms.CharField(max_length=250, required=False)
    link_lattes = forms.CharField(max_length=250, required=False)
    link_github = forms.CharField(max_length=250, required=False)

    cep = forms.CharField(max_length=15, required=False)
    rua = forms.CharField(max_length=150)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=20, required=False)
    bairro = forms.CharField(max_length=60, required=False)
    cidade = forms.CharField(max_length=60)
    estado = forms.CharField(max_length=2)
    

    def clean_matricula(self):
        m = self.cleaned_data['matricula']
        id = self.cleaned_data['id']

        try:
            if Egresso.objects.get(matricula=m).pk != id:
                raise forms.ValidationError('A matrícula fornecida já foi cadastrada.')
        except Egresso.DoesNotExist:
            pass

        return m


    def clean_data_nascimento(self):
        d = self.cleaned_data['data_nascimento']
        return '%d-%d-%d'%(d.year,d.month,d.day) 
    
    def clean_link_linkedin(self):
        return EgressoForm.urlize(self.cleaned_data['link_linkedin'])
    
    def clean_link_lattes(self):
        return EgressoForm.urlize(self.cleaned_data['link_lattes'])

    def clean_link_github(self):
        return EgressoForm.urlize(self.cleaned_data['link_github'])

    def urlize(texto):
        if re.match('http[s]{0,1}://', texto):
            return texto
        return 'http://%s'%texto if texto else ''





class FormacaoForm(forms.Form):
    nivel_formacao_id = forms.IntegerField(error_messages={'required': 'Selecione o nível do curso'})
    curso_id = forms.IntegerField(error_messages={'required': 'Selecione o nome do curso'}) #forms.CharField(max_length=80)
    area_id = forms.IntegerField(required=False) #forms.CharField(max_length=100, required=False)
    ano_inicio = forms.IntegerField()
    ano_termino = forms.IntegerField()


    def clean(self):
        cleaned_data = super(FormacaoForm, self).clean()
        inicio = cleaned_data.get('ano_inicio')
        termino = cleaned_data.get('ano_termino')
        if (inicio and termino) and (inicio > termino):
            raise forms.ValidationError('O ano de início deve ser menor que o ano de término.')
    