from django import forms
from SEGUE import settings
from .models import Egresso, Endereco, Formacao_Academica
import re

class EgressoForm(forms.Form):
    id = forms.IntegerField(required=False)
    user_id = forms.IntegerField()
    matricula = forms.CharField(max_length=30)
    nome_completo = forms.CharField(help_text=100)  
    data_nascimento = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    cpf = forms.CharField(max_length=15, required=False)
    identidade = forms.CharField(max_length=15, required=False)

    link_linkedin = forms.CharField(max_length=250, required=False)
    link_lattes = forms.CharField(max_length=250, required=False)
    link_github = forms.CharField(max_length=250, required=False)

    endereco_id = forms.IntegerField(required=False)
    cep = forms.CharField(max_length=15, required=False)
    rua = forms.CharField(max_length=150)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=20, required=False)
    bairro = forms.CharField(max_length=60, required=False)
    cidade = forms.CharField(max_length=60)
    estado = forms.CharField(max_length=2)
    

    def clean_matricula(self):
        mat = self.cleaned_data['matricula']
        id = self.cleaned_data['id']

        try:
            if Egresso.objects.get(matricula=mat).pk != id:
                raise forms.ValidationError('A matrícula fornecida já foi cadastrada.')
        except Egresso.DoesNotExist:
            pass

        return mat


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

    def form_to_dict_egresso(self):
        form_dict = self.cleaned_data
        return {
            'pk': form_dict['id'],
            'user_id': form_dict['user_id'],
            'matricula': form_dict['matricula'],
            'nome_completo': form_dict['nome_completo'],
            'data_nascimento': form_dict['data_nascimento'],
            'cpf': form_dict['cpf'],
            'identidade': form_dict['identidade'],
            'link_linkedin': form_dict['link_linkedin'],
            'link_lattes': form_dict['link_lattes'],
            'link_github': form_dict['link_github']
        }
    
    def form_to_dict_endereco(self):
        form_dict = self.cleaned_data
        return {
            'pk': form_dict['endereco_id'],
            'cep': form_dict['cep'],
            'rua': form_dict['rua'],
            'numero': form_dict['numero'],
            'complemento': form_dict['complemento'],
            'bairro': form_dict['bairro'],
            'cidade': form_dict['cidade'],
            'estado': form_dict['estado'],
        }


    def save(self, commit=True):
        # Obtém o endereço a ser adicionado ou editado
        endereco_update = Endereco( **self.form_to_dict_endereco() )

        # Obtém o egresso a ser adicionado ou editado
        egresso_update = Egresso( **self.form_to_dict_egresso() )

        if commit:
            endereco_update.save()
            egresso_update.endereco_id = endereco_update.pk
            egresso_update.save()

        return egresso_update, endereco_update





class FormacaoForm(forms.Form):
    egresso_id = forms.IntegerField()
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

    def form_to_dict_formacao(self):
        dict_form = self.cleaned_data
        return {
            'egresso_id': dict_form['egresso_id'],
            'curso_id': dict_form['curso_id'],
            'nivel_formacao_id': dict_form['nivel_formacao_id'],
            'area_id': dict_form['area_id'],
            'ano_inicio': dict_form['ano_inicio'],
            'ano_termino': dict_form['ano_termino'],
        }

    def save(self, commit=True):
        formacao = Formacao_Academica(**self.form_to_dict_formacao())

        if commit:
            formacao.save()
        return formacao
    