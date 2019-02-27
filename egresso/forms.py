from django import forms

class EgressoForm(forms.Form):
    matricula = forms.CharField(
        max_length=30,
        help_text='1')
    nome_completo = forms.CharField(
        help_text='2'
    )  
    data_nascimento = forms.DateField(
        help_text='3'
    )
    cpf = forms.CharField(
        max_length=15,
        help_text='4'
    )
    identidade = forms.CharField(
        max_length=15,
        help_text='5'
    )

    link_likedin = forms.CharField(
        help_text='6'
    )
    link_lattes = forms.CharField(
        help_text='7'
    )

    cep = forms.CharField(
        max_length=15,
        help_text='8'
    )
    rua = forms.CharField(
        max_length=150,
        help_text='9'
    )
    numero = forms.IntegerField(
        help_text='10'
    )
    bairro = forms.CharField(
        max_length=60, 
        help_text='11'
    )
    cidade = forms.CharField(
        max_length=60,
        help_text='12'
    )
    estado = forms.CharField(
        max_length=2,
        help_text='13'
    )

    def clean(self):
        cleaned_data = super(EgressoForm, self).clean()
        '''
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')'''

        #if not name and not email and not message:
            #raise forms.ValidationError('You have to write something!')

        return cleaned_data
