from django import forms
from SEGUE import settings
from .models import Egresso, Endereco, Formacao, DadosPessoais, obter_egresso, PerfilSites
from curso.models import Curso
import re

class DadosPessoaisForm(forms.ModelForm):
    class Meta:
        model = DadosPessoais
        exclude = ['genero', 'estado_civil']

    estado_civil_id = forms.IntegerField(required=False)
    genero_id = forms.IntegerField(required=False)
    egresso_id = forms.IntegerField()

    """
    def clean_matricula(self):
        mat = self.cleaned_data['matricula']
        id = self.cleaned_data['id']

        try:
            if Egresso.objects.get(matricula=mat).pk != id:
                raise forms.ValidationError('A matrícula fornecida já foi cadastrada.')
        except Egresso.DoesNotExist:
            pass

        return mat
    """

    def clean_data_nascimento(self):
        d = self.cleaned_data['data_nascimento']
        return '%d-%d-%d'%(d.year,d.month,d.day)

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        egresso = obter_egresso(id=cleaned_data['egresso_id'])
        del cleaned_data['egresso_id']
        dados_pessoais = DadosPessoais( **cleaned_data )

        if commit:
            dados_pessoais.save()
            egresso.dados_id = dados_pessoais.pk
            egresso.save()

        return dados_pessoais


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        exclude = []

    egresso_id = forms.IntegerField()

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        egresso = obter_egresso(id=cleaned_data['egresso_id'])
        del cleaned_data['egresso_id']
        endereco = Endereco( **cleaned_data )

        if commit:
            endereco.save()
            egresso.endereco_id = endereco.pk
            egresso.save()

        return endereco


class PerfilSitesForm(forms.ModelForm):
    class Meta:
        model = PerfilSites
        exclude = []

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


class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = ['ano_inicio', 'ano_termino']

    # Permite selecionar a TAB correta no template
    tipo_curso = forms.CharField(initial='curso-externo')

    egresso_id = forms.IntegerField()
    curso_id = forms.IntegerField(required=False)
    nome = forms.CharField(required=False)
    nivel_curso_id = forms.IntegerField(required=False)
    area_atuacao_id = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(FormacaoForm, self).clean()

        print('\n\n', cleaned_data['tipo_curso'], '\n\n')
        inicio = cleaned_data.get('ano_inicio')
        termino = cleaned_data.get('ano_termino')
        if (inicio and termino) and inicio > termino:
            cleaned_data['inicio'] = termino
            cleaned_data['termino'] = inicio

        return cleaned_data
        
    def clean_nome(self):
        tipo_curso = self.cleaned_data.get('tipo_curso')
        nome = self.cleaned_data.get('nome')

        if tipo_curso == 'curso-externo' and not nome:
            raise forms.ValidationError('Foneça o nome do curso')

        return nome

    def clean_nivel_curso_id(self):
        tipo_curso = self.cleaned_data.get('tipo_curso')
        nivel_curso_id = self.cleaned_data.get('nivel_curso_id')

        if tipo_curso == 'curso-externo' and not nivel_curso_id:
            raise forms.ValidationError('Selecione o nível do curso')

        return nivel_curso_id

    def clean_area_atuacao_id(self):
        tipo_curso = self.cleaned_data.get('tipo_curso')
        area_atuacao_id = self.cleaned_data.get('area_atuacao_id')

        if tipo_curso == 'curso-externo' and not area_atuacao_id:
            raise forms.ValidationError('Selecione o área de atuação')

        return area_atuacao_id

    def form_to_dict_formacao(self):
        dict_form = self.clean()
        return {
            'egresso_id': dict_form['egresso_id'],
            'curso_id': dict_form['curso_id'],
            'ano_inicio': dict_form['ano_inicio'],
            'ano_termino': dict_form['ano_termino'],
        }

    def form_to_dict_curso(self):
        dict_form = self.clean()
        return {
            'id': dict_form['curso_id'],
            'nome': dict_form['nome'],
            'nivel_curso_id': dict_form['nivel_curso_id'],
            'area_atuacao_id': dict_form['area_atuacao_id'],
        }

    def save(self, commit=True):
        data = self.clean()
        formacao = Formacao(**self.form_to_dict_formacao())

        curso = None
        if data['tipo_curso'] == 'curso-externo':
            curso = Curso(**self.form_to_dict_curso())    

        if commit:
            if curso:
                curso.save()
                formacao.curso_id = curso.pk
            else:
                formacao.curso_id = data['curso_id']
            
            formacao.save()

        return formacao
    