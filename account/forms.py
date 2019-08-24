from django import forms
from django.forms.models import model_to_dict
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from egresso.models import Egresso, DadosPessoais, Formacao
from empresa.models import Empresa

from .models import User, TipoUsuario


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'tipo_usuario')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.username = user.email.rpartition('@')[0]
        user.set_password(self.cleaned_data["password"])
        user.save()

        user_especifico = None
        if user.tipo_usuario.pk == 2:
            dados = DadosPessoais(nome_completo=user.username)
            dados.save()
            user_especifico = Egresso(dados=dados)
        elif user.tipo_usuario.pk == 3:
            user_especifico = Empresa()
        else:
            return user

        user_especifico.user = user
        user_especifico.save()
        
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'tipo_usuario', 'password' , 'is_active', 'is_trusty')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def save(self, commit=True):
        user = super(UserAdminChangeForm, self).save(commit=False)
        if commit:
            user.save()
        return user



class EgressoForm(forms.ModelForm):
    nome_completo = forms.CharField()
    password = forms.CharField()
    curso_id = forms.IntegerField()
    ano_inicio = forms.IntegerField()
    ano_termino = forms.IntegerField()

    class Meta:
        model = User
        fields = ('email', )

    def form_to_dict_formacao(self):
        dict_form = self.cleaned_data
        return {
            'curso_id': dict_form['curso_id'],
            'ano_inicio': dict_form['ano_inicio'],
            'ano_termino': dict_form['ano_termino'],
        }

    def save(self, commit=True):
        data = self.cleaned_data
        user = super(EgressoForm, self).save(commit=False)

        nome = data['nome_completo']
        user.username = nome.partition(' ')[0] if ' ' in nome else nome
        user.set_password(data["password"])
        user.tipo_usuario_id = 2
    
        dados_pessoais = DadosPessoais(nome_completo=data['nome_completo'])
        egresso = Egresso()
        formacao = Formacao(**self.form_to_dict_formacao())

        if commit:
            user.save()
            
            dados_pessoais.save()

            egresso.user=user
            egresso.dados=dados_pessoais
            egresso.save()

            formacao.egresso = egresso
            formacao.save()

        return user