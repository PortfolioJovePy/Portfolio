from django import forms
from .models import *

class FormularioContato(forms.ModelForm):
    def __init__(self, *args, font_class='',idioma='portugues', **kwargs):
        super(FormularioContato, self).__init__(*args, **kwargs)
        classes_base = 'form-control mb-2'
        self.fields['nome'].widget.attrs['class'] = f"{classes_base} {font_class}"
        self.fields['email'].widget.attrs['class'] = f"{classes_base} {font_class}"
        self.fields['mensagem'].widget.attrs['class'] = f"{classes_base} {font_class}"
        if idioma == 'portugues':
            mensagem = 'Sobre o que você quer conversar?'
            nome = 'Nome'
            email = 'Seu e-mail'
        else:
            mensagem = 'What do you want to talk about?'
            nome = 'Name'
            email = 'Your e-mail'
        self.fields['nome'].widget.attrs['placeholder'] = nome
        self.fields['mensagem'].widget.attrs['placeholder'] = mensagem
        self.fields['email'].widget.attrs['placeholder'] = email
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control mb-2','placeholder': 'Apresente-se'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'E-mail'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control mb-2', 'placeholder': 'Placeholder padrão', 'rows': 6}),
        }
        labels = {
            'nome': '',
            'email': '',
            'mensagem': ''
        }

class FormularioNewsletter(forms.ModelForm):      
    def __init__(self, *args,idioma='portugues', **kwargs):
        super(FormularioNewsletter, self).__init__(*args, **kwargs)
        classes_base = 'form-control mt-4'        
        self.fields['email'].widget.attrs['class'] = f"{classes_base}"
        if idioma == 'portugues':            
            email = 'Seu e-mail'
        else:            
            email = 'Your e-mail'
        self.fields['email'].widget.attrs['placeholder'] = email        
        self.fields['email'].label = ''
        
    class Meta:
        model = Newsletter
        fields = ['email']
        error_messages = {
                'email': {
                    'unique': "Este e-mail já está cadastrado em nossa Newsletter."
                }
            }