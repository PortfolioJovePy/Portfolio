from django import forms
from .models import *

class FormularioContato(forms.ModelForm):
    def __init__(self, *args, font_class='',idioma='portugues', **kwargs):
        super(FormularioContato, self).__init__(*args, **kwargs)
        # Adiciona a classe font dinamicamente
        classes_base = 'form-control mb-2'
        self.fields['nome'].widget.attrs['class'] = f"{classes_base} {font_class}"
        self.fields['email'].widget.attrs['class'] = f"{classes_base} {font_class}"
        self.fields['mensagem'].widget.attrs['class'] = f"{classes_base} {font_class}"
        if idioma == 'portugues':
            mensagem = 'Sobre o que você quer conversar?'
            nome = 'Nome'
        else:
            mensagem = 'What do you want to talk about?'
            nome = 'Name'
        self.fields['nome'].widget.attrs['placeholder'] = nome
        self.fields['mensagem'].widget.attrs['placeholder'] = mensagem
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
    class Meta:
        model = Newsletter
        fields = ['email']
       